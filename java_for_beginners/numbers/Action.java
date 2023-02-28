package numbers;

enum Action {
    EMPTY,
    EXIT("Goodbye!"),
    INVALID_NUMBER("The first parameter should be a natural number or zero."),
    INVALID_COUNT("The second parameter should be a natural number."),
    INVALID_QUERY_PROPERTY("The %s %s %s wrong.%nAvailable properties: %s"),
    MUTUALLY_EXCLUSIVE_PROPERTIES("""
            The request contains mutually exclusive properties: %s
            There are no numbers with these properties.""");
    private String message;

    Action() {
        this("");
    }

    Action(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
