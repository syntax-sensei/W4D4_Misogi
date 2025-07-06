def categorize_query(query):
    keywords = {
        "leave": ["vacation", "sick leave", "paid time off", "leave"],
        "benefits": ["insurance", "medical", "perks", "bonus", "benefits"],
        "remote": ["remote", "work from home", "hybrid"],
        "conduct": ["code of conduct", "ethics", "behavior"],
        "enrollment": ["enroll", "joining", "probation"]
    }
    for category, words in keywords.items():
        if any(word in query.lower() for word in words):
            return category
    return "general"
