from src.rag.retriever import retrieve
from src.rag.prompt_builder import build_prompt
from src.core.llm import generate_response

def chat(query, state=None):
    if state is None:
        state = {}
        
    q = query.lower().strip("?.! ")
    
    # Load DataFrame for lookups
    try:
        from src.utils.db_helper import load_products_df
        df = load_products_df()
    except Exception:
        df = None
        
    # Check query type
    is_avail = ("available" in q or "avaliable" in q or "availabel" in q or 
                "do you have" in q or "have you got" in q or 
                "do you sell" in q or "is there" in q or q.endswith("available") or q.endswith("avaliable"))
    
    is_price = ("price" in q or "cost" in q or "rate" in q or "how much" in q)
    is_expiry = ("expiry" in q or "expriy" in q or "expire" in q or "date" in q)
    is_loc = ("located" in q or "location" in q or "where" in q or "place" in q or "supermarket" in q or "departmental store" in q)
    
    # Extract search term for product identification
    search_term = q
    
    # Remove common question prefixes and suffixes
    prefixes = [
        "is ", "are ", "do you have ", "have you got ", "do you sell ", "is there ", "any ", "where is ",
        "what is the price of ", "what is the cost of ", "what is the expiry of ", "what is the expiry date of ",
        "what is the location of ", "where can i find ", "how much is ", "price of ", "cost of ", "location of ",
        "expiry of ", "expiry date of ", "show me "
    ]
    for p in prefixes:
        if search_term.startswith(p):
            search_term = search_term[len(p):]
            
    suffixes = [
        " available", " avaliable", " availabel", " in stock", " present", " is", " are",
        " located", " location", " price", " cost", " expiry", " expiry date"
    ]
    for s in suffixes:
        if search_term.endswith(s):
            search_term = search_term[:-len(s)]
            
    search_term = search_term.strip("?.! ")
    
    # Try to find a matching product in the database to update the active_product
    matched_prod = None
    if search_term and df is not None:
        # Match product Name or Category
        matches = df[
            df['Name'].str.lower().str.contains(search_term) | 
            df['Category'].str.lower().str.contains(search_term)
        ]
        if not matches.empty:
            matched_prod = matches.iloc[0].to_dict()
            state["active_product"] = matched_prod
            
    # Retrieve active product from state
    active_product = state.get("active_product")
    
    # 1. Product Availability Query (explicitly asked, or if no other query types matched but we matched a product)
    if (is_avail or (not is_price and not is_expiry and not is_loc)) and df is not None:
        if matched_prod:
            fallback_resp = f"Yes, {matched_prod['Name']} is available."
            system_prompt = f"The user is asking if a product is available. We found '{matched_prod['Name']}' in category '{matched_prod['Category']}' in stock ({matched_prod['Stock Quantity']} units). Reply yes, and mention the product name."
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
            try:
                response = generate_response(messages)
                if "Unable to generate" in response or not response:
                    response = fallback_resp
            except Exception:
                response = fallback_resp
            return response
        else:
            # If the user explicitly asked for availability, but no match was found
            if is_avail and search_term:
                fallback_resp = f"No, {search_term} is not available."
                system_prompt = f"The user is asking if '{search_term}' is available, but it is not in our inventory. Reply politely that it is not available."
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ]
                try:
                    response = generate_response(messages)
                    if "Unable to generate" in response or not response:
                        response = fallback_resp
                except Exception:
                    response = fallback_resp
                return response
            # Otherwise, fall through to default RAG pipeline
            
    # 2. Price Query
    if is_price and active_product:
        fallback_resp = f"The price of {active_product['Name']} is {active_product['Price/RS']} RS."
        system_prompt = f"The user is asking for the price of the active product: '{active_product['Name']}'. The price is {active_product['Price/RS']} RS. Reply with this price."
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
        try:
            response = generate_response(messages)
            if "Unable to generate" in response or not response:
                response = fallback_resp
        except Exception:
            response = fallback_resp
        return response

    # 3. Expiry Query
    if is_expiry and active_product:
        fallback_resp = f"The expiry date of {active_product['Name']} is {active_product['Expiry Date']}."
        system_prompt = f"The user is asking for the expiry date of the active product: '{active_product['Name']}'. The expiry date is {active_product['Expiry Date']}. Reply with this expiry date."
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
        try:
            response = generate_response(messages)
            if "Unable to generate" in response or not response:
                response = fallback_resp
        except Exception:
            response = fallback_resp
        return response

    # 4. Location Query
    if is_loc and active_product:
        fallback_resp = f"It is located in Block {active_product['Block Name']}, Rack {active_product['Rack No']}, Section: {active_product['Session']}."
        system_prompt = f"The user is asking where the active product '{active_product['Name']}' is located. It is located in Block {active_product['Block Name']}, Rack {active_product['Rack No']}, Section {active_product['Session']}. Reply with this location information."
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
        try:
            response = generate_response(messages)
            if "Unable to generate" in response or not response:
                response = fallback_resp
        except Exception:
            response = fallback_resp
        return response

    # Default RAG pipeline fallback
    context = retrieve(query)
    prompt = build_prompt(query, context)
    try:
        response = generate_response([{"role": "user", "content": prompt}])
    except Exception:
        response = "I'm sorry, I couldn't process your request. Please try again."
    return response

# Alias to support both api/chat and streamlit_app imports
ask = chat