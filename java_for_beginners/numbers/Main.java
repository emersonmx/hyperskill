package numbers;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        System.out.println("Welcome to Amazing Numbers!");
        System.out.println();
        showInstructions();

        while (true) {
            Input input = new Input();
            Action action = input.getAction(getInput("Enter a request: "));
            if (action == null) {
                showInput(input);
            } else if (action == Action.EXIT) {
                System.out.println(action.getMessage());
                break;
            } else if (action == Action.INVALID_NUMBER) {
                System.out.println(action.getMessage());
            } else if (action == Action.INVALID_COUNT) {
                System.out.println(action.getMessage());
            } else if (action == Action.INVALID_QUERY_PROPERTY) {
                System.out.println(action.getMessage());
            } else if (action == Action.MUTUALLY_EXCLUSIVE_PROPERTIES) {
                System.out.println(action.getMessage());
            }
        }
    }

    private static void showInput(Input input) {
        ANumber number = input.getNumber();
        int count = input.getCount();
        Query[] queries = input.getQueries();

        if (number == null) {
            throw new IllegalArgumentException("Number is required!");
        }

        if (queries != null) {
            showNumbersByProperty(number, count, queries);
            return;
        }

        if (count == -1) {
            showNumber(number);
        } else {
            showNumbers(number, count);
        }
    }

    private static void showNumber(ANumber number) {
        System.out.printf("Properties of %d%n", number.getValue());
        System.out.printf("%12s: %s%n", "buzz", number.isBuzz());
        System.out.printf("%12s: %s%n", "duck", number.isDuck());
        System.out.printf("%12s: %s%n", "palindromic", number.isPalindromic());
        System.out.printf("%12s: %s%n", "gapful", number.isGapful());
        System.out.printf("%12s: %s%n", "spy", number.isSpy());
        System.out.printf("%12s: %s%n", "square", number.isSquare());
        System.out.printf("%12s: %s%n", "sunny", number.isSunny());
        System.out.printf("%12s: %s%n", "jumping", number.isJumping());
        System.out.printf("%12s: %s%n", "happy", number.isHappy());
        System.out.printf("%12s: %s%n", "sad", number.isSad());
        System.out.printf("%12s: %s%n", "even", number.isEven());
        System.out.printf("%12s: %s%n", "odd", number.isOdd());
    }

    private static String getInlineNumberProperties(ANumber number) {
        StringBuilder builder = new StringBuilder();
        builder.append(number.getValue()).append(" is ");
        if (number.isBuzz()) {
            builder.append("buzz, ");
        }
        if (number.isDuck()) {
            builder.append("duck, ");
        }
        if (number.isPalindromic()) {
            builder.append("palindromic, ");
        }
        if (number.isGapful()) {
            builder.append("gapful, ");
        }
        if (number.isSpy()) {
            builder.append("spy, ");
        }
        if (number.isSquare()) {
            builder.append("square, ");
        }
        if (number.isSunny()) {
            builder.append("sunny, ");
        }
        if (number.isJumping()) {
            builder.append("jumping, ");
        }
        if (number.isHappy()) {
            builder.append("happy, ");
        }
        if (number.isSad()) {
            builder.append("sad, ");
        }
        if (number.isEven()) {
            builder.append("even, ");
        }
        if (number.isOdd()) {
            builder.append("odd");
        }

        String result = builder.toString();
        return result.replaceAll(", $", "");
    }

    private static void showNumbers(ANumber number, int count) {
        for (int i = 0; i < count; i++) {
            String properties = getInlineNumberProperties(new ANumber(number.getValue() + i));
            System.out.println(properties);
        }
    }

    private static void showNumbersByProperty(ANumber number, int count, Query[] queries) {
        int i = 0;
        int k = 0;
        while (k < count) {
            String inlineProperties = getInlineNumberProperties(new ANumber(number.getValue() + i));

            boolean hasProperty = true;
            for (Query query : queries) {
                String property = query.getProperty().toString().toLowerCase();
                boolean found = inlineProperties.indexOf(property) != -1;
                if (query.getOperator() == Query.Operator.NOT) {
                    found = !found;
                }
                hasProperty = hasProperty && found;
            }

            if (hasProperty) {
                System.out.println(inlineProperties);
                k++;
            }
            i++;
        }
    }

    private static void showInstructions() {
        System.out.println("""
                Supported requests:
                - enter a natural number to know its properties;
                - enter two natural numbers to obtain the properties of the list:
                  * the first parameter represents a starting number;
                  * the second parameter shows how many consecutive numbers are to be printed;
                - two natural numbers and properties to search for;
                - a property preceded by minus must not be present in numbers;
                - separate the parameters with one space;
                - enter 0 to exit.""");
    }

    private static String getInput(String message) {
        Scanner scanner = new Scanner(System.in);
        System.out.printf(message);
        return scanner.nextLine();
    }
}
