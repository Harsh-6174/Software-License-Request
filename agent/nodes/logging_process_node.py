def logging_process_node(state):
    print("--------------------------- Final State After All Nodes ---------------------------")
    for key,value in state.items():
        print(f"{key} : {value}")
    
    return state