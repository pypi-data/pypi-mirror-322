def llm_function(func):
    func._is_llm_function = True
    return func
