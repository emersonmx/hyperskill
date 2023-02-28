package numbers;

import java.util.Arrays;
import java.util.Objects;

class Query {
    enum Operator {
        NONE, NOT;

        public Operator invert() {
            return this == Operator.NONE ? Operator.NOT : Operator.NONE;
        }

        public static Operator fromChar(char operator) {
            if (operator == '-') {
                return NOT;
            }
            return NONE;
        }

        @Override
        public String toString() {
            if (this == NOT) {
                return "-";
            }
            return "";
        }
    }

    private Property property;
    private Operator operator = Operator.NONE;

    public Query(Operator operator, Property property) {
        this.property = property;
        this.operator = operator == null ? Operator.NONE : operator;
    }

    public Query invert() {
        return new Query(operator.invert(), property);
    }

    public Property getProperty() {
        return property;
    }

    public Operator getOperator() {
        return operator;
    }

    public static Query fromString(String query) {
        String property = query.toUpperCase().trim();
        Operator operator = Operator.fromChar(property.charAt(0));
        if (operator != Operator.NONE) {
            property = property.substring(1);
        }
        if (Property.has(property)) {
            return new Query(operator, Property.valueOf(property));
        }
        return null;
    }

    public static Query[] fromStringList(String queries) {
        String[] rawQueries = queries.toUpperCase().trim().split(",");
        Query[] result = new Query[rawQueries.length];
        int i = 0;
        for (int k = 0; k < rawQueries.length; k++) {
            String value = rawQueries[k].trim();
            Query query = fromString(value);
            if (query != null) {
                result[i] = query;
                i++;
            }
        }
        return Arrays.copyOfRange(result, 0, i);
    }

    public static Query[] fromStringList(String[] queries) {
        return fromStringList(String.join(",", queries));
    }

    public static String[] toStringList(Query[] queries) {
        StringBuilder builder = new StringBuilder();
        for (Query query : queries) {
            builder.append(query).append(",");
        }
        String result = builder.toString();
        if (result.isEmpty()) {
            return new String[0];
        }
        return result.split(",");
    }

    @Override
    public String toString() {
        String op = operator.toString();
        String prop = property == null ? "" : property.toString();
        return op + prop;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Query query = (Query) o;
        return property == query.property && operator == query.operator;
    }

    @Override
    public int hashCode() {
        return Objects.hash(property, operator);
    }
}
