import java.util.Random;
import java.util.Scanner;

public class BullsCows {
    private static final String CHARS = "0123456789abcdefghijklmnopqrstuvwxyz";

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Input the length of the secret code:");
        System.out.print("> ");
        String input = scanner.nextLine();
        int length;
        try {
            length = Integer.parseInt(input);
        } catch (NumberFormatException e) {
            System.out.println("Error: \"%s\" isn't a valid number.".formatted(input));
            return;
        }

        System.out.println("Input the number of possible symbols in the code:");
        System.out.print("> ");
        int symbols = Integer.parseInt(scanner.nextLine());
        if (length <= 0 || length > symbols || symbols > CHARS.length()) {
            System.out.println("""
                    Error: it's not possible to generate a code with a length of %d with %d unique symbols.
                    """.formatted(length, symbols));
            return;
        }
        String secret = generateSecret(length, symbols);

        String secretMask = new String("*").repeat(length);
        StringBuilder builder = new StringBuilder("(");

        builder.append("0-").append(symbols >= 10 ? 9 : symbols);
        if (symbols > 10) {
            builder.append(", ").append("a-").append(CHARS.charAt(symbols - 1));
        }
        builder.append(")");

        System.out.println("The secret is prepared: %s %s.".formatted(secretMask, builder));
        System.out.println("Okay, let's start a game!");
        int turn = 1;
        input = "";
        while (!input.equals(secret)) {
            System.out.println("Turn %d:".formatted(turn));
            System.out.print("> ");
            input = scanner.nextLine();

            int bulls = countBulls(secret, input);
            int cows = countCows(secret, input);
            String grade = getGrade(bulls, cows);

            System.out.println(grade);
            turn++;
        }
        System.out.println("Congratulations! You guessed the secret code.");
    }

    private static int countBulls(String secret, String input) {
        int bulls = 0;

        for (int i = 0; i < secret.length(); i++) {
            char c = input.charAt(i);
            if (secret.contains(String.valueOf(c))) {
                if (secret.charAt(i) == c) {
                    bulls++;
                }
            }
        }
        return bulls;
    }

    private static int countCows(String secret, String input) {
        int cows = 0;

        for (int i = 0; i < secret.length(); i++) {
            char c = input.charAt(i);
            if (secret.contains(String.valueOf(c))) {
                if (secret.charAt(i) != c) {
                    cows++;
                }
            }
        }
        return cows;
    }

    private static String getGrade(int bulls, int cows) {
        String grade = "None";
        if (bulls > 0 && cows > 0) {
            grade = "%d bull(s) and %d cow(s)".formatted(bulls, cows);
        } else if (bulls > 0) {
            grade = "%d bull(s)".formatted(bulls);
        } else if (cows > 0) {
            grade = "%d cow(s)".formatted(cows);
        }
        return "Grade: %s".formatted(grade);
    }

    private static String generateSecret(int length, int symbols) {
        Random rng = new Random();
        StringBuilder builder = new StringBuilder();
        if (length <= 0) {
            return "";
        }
        while (builder.length() < length) {
            int index = rng.nextInt(symbols);
            String c = String.valueOf(CHARS.charAt(index));
            if (builder.length() == 0 && c.equals("0")) {
                continue;
            }
            if (builder.indexOf(c) == -1) {
                builder.append(c);
            }
        }
        return builder.toString();
    }
}
