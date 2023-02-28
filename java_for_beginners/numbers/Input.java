package numbers;

import java.util.Arrays;

class Input {
    private String cleanedInput;
    private String[] inputs;
    private ANumber number;
    private int count = -1;
    private Query[] queries = null;

    public ANumber getNumber() {
        return number == null ? null : new ANumber(number.getValue());
    }

    int getCount() {
        return count;
    }

    public Query[] getQueries() {
        return queries == null ? null : queries.clone();
    }

    public Action getAction(String input) {
        this.cleanedInput = input.toUpperCase().trim();
        this.inputs = this.cleanedInput.split(" ");
        return parseInputs();
    }

    private Action parseInputs() {
        if (inputs.length == 0) {
            return Action.EMPTY;
        }

        Action action = checkExit();
        if (action != null) {
            return action;
        }

        action = checkInvalidNumber();
        if (action != null) {
            return action;
        }

        if (inputs.length > 1) {
            action = checkInvalidCount();
            if (action != null) {
                return action;
            }
        }

        if (inputs.length > 2) {
            action = checkInvalidQueryProperty();
            if (action != null) {
                return action;
            }

            action = checkMutualExclusiveProperties();
            if (action != null) {
                return action;
            }
        }

        return null;
    }

    private String[] getPropertyStrings() {
        return Arrays.copyOfRange(inputs, 2, inputs.length);
    }

    private String[] getValidPropertyStrings() {
        Query[] validQueries = Query.fromStringList(getPropertyStrings());
        return Query.toStringList(validQueries);
    }

    private String[] getInvalidPropertyStrings() {
        String[] properties = getPropertyStrings();
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < properties.length; i++) {
            Query query = Query.fromString(properties[i]);
            if (query == null) {
                builder.append(properties[i]).append(",");
            }
        }
        String result = builder.toString().replaceAll(",$", "").trim();
        if (result.isEmpty()) {
            return new String[0];
        }
        return result.split(",");
    }

    private Action checkExit() {
        if (inputs[0].equals("0")) {
            return Action.EXIT;
        }
        return null;
    }

    private Action checkInvalidNumber() {
        String input = inputs[0];
        if (!input.matches("\\d+")) {
            return Action.INVALID_NUMBER;
        }
        this.number = new ANumber(input);
        return null;
    }

    private Action checkInvalidCount() {
        String input = inputs[1];
        if (!input.matches("\\d+")) {
            return Action.INVALID_COUNT;
        }
        this.count = Integer.parseInt(input);
        return null;
    }

    private Action checkInvalidQueryProperty() {
        String[] invalidQueries = getInvalidPropertyStrings();
        int wrongCount = invalidQueries.length;
        if (wrongCount > 0) {
            Action action = Action.INVALID_QUERY_PROPERTY;
            String rawMessage = action.getMessage();
            String verb = wrongCount == 1 ? "is" : "are";
            String noun = wrongCount == 1 ? "property" : "properties";
            action.setMessage(rawMessage.formatted(noun, Arrays.toString(invalidQueries), verb, Arrays.toString(Property.values())));
            return action;
        }
        this.queries = Query.fromStringList(getValidPropertyStrings());
        return null;
    }

    private Action checkMutualExclusiveProperties() {
        Query[] queries = Query.fromStringList(getValidPropertyStrings());
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < queries.length; i++) {
            Query needle = queries[i];
            for (int j = 0; j < queries.length; j++) {
                Query check = queries[j];
                boolean hasInverseQuery = hasInverseQuery(needle, check);
                boolean hasMutualExclusive = hasMutualExclusive(needle, check);
                if ((hasInverseQuery || hasMutualExclusive) && builder.indexOf(needle.toString()) == -1) {
                    builder.append(needle).append(",").append(check).append(",");
                }
            }
        }

        String errors = builder.toString().replaceAll(",$", "").trim();
        if (!errors.isEmpty()) {
            Action result = Action.MUTUALLY_EXCLUSIVE_PROPERTIES;
            String rawMessage = result.getMessage();
            result.setMessage(rawMessage.formatted("[%s]".formatted(errors)));
            return result;
        }

        return null;
    }

    private static boolean hasInverseQuery(Query needle, Query check) {
        Property needleProperty = needle.getProperty();
        Query.Operator needleOperator = needle.getOperator();
        Property checkProperty = check.getProperty();
        Query.Operator checkOperator = check.getOperator();
        return needleProperty == checkProperty && !(needleOperator == checkOperator);
    }

    private static boolean hasMutualExclusive(Query first, Query second) {
        if (first.equals(second)) {
            return false;
        }

        Query[][] checks = new Query[][]{
                Query.fromStringList("even,odd"),
                Query.fromStringList("duck,spy"),
                Query.fromStringList("sunny,square"),
                Query.fromStringList("happy,sad"),
                Query.fromStringList("-even,-odd"),
                Query.fromStringList("-duck,-spy"),
                Query.fromStringList("-sunny,-square"),
                Query.fromStringList("-happy,-sad"),
        };

        for (int i = 0; i < checks.length; i++) {
            Query firstCheck = checks[i][0];
            Query secondCheck = checks[i][1];
            if (first.equals(firstCheck) && second.equals(secondCheck)) {
                return true;
            }
            if (first.equals(secondCheck) && second.equals(firstCheck)) {
                return true;
            }
        }

        return false;
    }
}
