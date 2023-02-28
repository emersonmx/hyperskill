import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.RoundingMode;
import java.util.Scanner;

public class NumberBaseConverter {
    enum State {
        MENU, CONVERTER, EXIT
    }

    private static State state = State.MENU;
    private static int sourceBase = 0;
    private static int targetBase = 0;

    public static void main(String[] args) {
        boolean running = true;
        while (running) {
            processInput();
            System.out.println();

            if (state == State.EXIT) {
                running = false;
            }
        }
    }

    private static String getInput() {
        Scanner scanner = new Scanner(System.in);
        return scanner.nextLine().replaceAll("\\s+", " ").trim();
    }

    private static void processInput() {
        switch (state) {
            case MENU:
                showMenu();
                break;
            case CONVERTER:
                showConverter();
                break;
            default:
                break;
        }
    }

    private static void showMenu() {
        System.out.print("Enter two numbers in format: {source base} {target base} (To quit type /exit) ");
        String input = getInput();
        if (input.equals("/exit")) {
            state = State.EXIT;
            return;
        } else if (input.isEmpty()) {
            return;
        }

        String[] inputs = input.split(" ");
        if (inputs.length != 2) {
            return;
        }

        sourceBase = Integer.parseInt(inputs[0]);
        targetBase = Integer.parseInt(inputs[1]);
        state = State.CONVERTER;
    }

    private static void showConverter() {
        System.out.printf("Enter number in base %d to convert to base %d (To go back type /back) ", sourceBase, targetBase);
        String input = getInput();
        if (input.equals("/back")) {
            state = State.MENU;
            return;
        } else if (input.isEmpty()) {
            return;
        }

        String result = convert(input);
        System.out.printf("Conversion result: %s%n", result);
    }

    private static String convert(String number) {
        String[] numbers = number.split("\\.");
        if (numbers.length == 1) {
            return convertInteger(numbers[0]);
        } else {
            String integer = convertInteger(numbers[0]);
            String fractional = convertFractional(numbers[1]);
            if (fractional.isEmpty()) {
                return integer;
            } else {
                return "%s.%s".formatted(integer, fractional);
            }
        }
    }

    private static String convertInteger(String number) {
        BigInteger asDecimal = new BigInteger(number, sourceBase);
        return asDecimal.toString(targetBase);
    }

    private static String convertFractional(String number) {
        BigDecimal targetBase = new BigDecimal(NumberBaseConverter.targetBase);
        BigDecimal result = convertFractionToBase10(number);
        BigDecimal integerPart = BigDecimal.ZERO;
        BigDecimal fractionalPart = result.subtract(integerPart);
        StringBuilder builder = new StringBuilder();
        while (fractionalPart.doubleValue() != 0.0 && builder.toString().length() < 5) {
            result = result.multiply(targetBase);
            integerPart = result.setScale(0, RoundingMode.DOWN);
            int c = integerPart.intValue();
            result = result.subtract(integerPart);
            fractionalPart = result;
            builder.append(Character.forDigit(c, NumberBaseConverter.targetBase));
        }

        String resultString = builder.toString();
        return (resultString + "00000").substring(0, 5);
    }

    private static BigDecimal convertFractionToBase10(String fraction) {
        BigDecimal result = BigDecimal.ZERO;
        for (int i = 0; i < fraction.length(); i++) {
            char c = fraction.charAt(i);
            long number = Character.getNumericValue(c);
            result = result.add(BigDecimal.valueOf(number * Math.pow(sourceBase, -(i + 1))));
        }
        return result;
    }
}

