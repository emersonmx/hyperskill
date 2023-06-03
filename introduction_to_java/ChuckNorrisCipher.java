import java.util.Scanner;
import java.util.regex.Pattern;

public class ChuckNorrisCipher {
    public static void main(String[] args) {
        boolean running = true;
        while (running) {
            String input = getInput("Please input operation (encode/decode/exit):%n");

            switch (input) {
                case "encode":
                    encodeAction();
                    break;
                case "decode":
                    decodeAction();
                    break;
                case "exit":
                    System.out.println("Bye!");
                    running = false;
                    break;
                default:
                    System.out.printf("There is no '%s' operation%n", input);
            }
            System.out.println();
        }
    }

    private static void encodeAction() {
        String input = getInput("Input string:%n");
        String binary = toBinaryString(input);
        System.out.printf("Encoded string:%n%s%n", encode(binary));
    }

    private static void decodeAction() {
        String input = getInput("Input encoded string:%n");
        String cleanInput = input.replaceAll(" +", " ").trim();

        if (isValidInput(cleanInput)) {
            String binary = decode(cleanInput);
            System.out.printf("Decoded string:%n%s%n", fromBinaryString(binary));
        } else {
            System.out.println("Encoded string is not valid.");
        }
    }

    private static boolean isValidInput(String input) {
        if (input.replaceAll("[^0 ]", "X").indexOf("X") != -1) {
            return false;
        }

        String[] parts = input.split(" ");
        if (parts.length % 2 != 0) {
            return false;
        }

        for (int i = 0; i < parts.length; i += 2) {
            String bit = parts[i];
            if (bit.length() > 2) {
                return false;
            }
        }

        String decoded = decode(input);
        if (decoded.length() % 7 != 0) {
            return false;
        }
        return true;
    }

    private static String getInput(String message) {
        Scanner scanner = new Scanner(System.in);
        System.out.printf(message);
        return scanner.nextLine();
    }

    private static String encode(String input) {
        StringBuilder builder = new StringBuilder();

        char lc = ' ';
        for (char c : input.toCharArray()) {
            if (c == lc) {
                builder.append('0');
            } else {
                builder.append(' ').append(c == '1' ? "0 0" : "00 0");
            }
            lc = c;
        }
        return builder.toString().trim();
    }

    private static String decode(String input) {
        String[] parts = input.split(" ");
        StringBuilder builder = new StringBuilder();

        for (int i = 0; i < parts.length; i += 2) {
            if (parts[i].length() == 1) {
                builder.append(new String("1").repeat(parts[i + 1].length()));
            } else {
                builder.append(new String("0").repeat(parts[i + 1].length()));
            }
        }
        return builder.toString();
    }

    private static String toBinaryString(String input) {
        StringBuilder builder = new StringBuilder();
        for (char c : input.toCharArray()) {
            String binary = "0000000" + Integer.toBinaryString(c);
            binary = binary.substring(binary.length() - 7);
            builder.append(binary);
        }
        return builder.toString();
    }

    private static String fromBinaryString(String input) {
        StringBuilder builder = new StringBuilder();
        final int byteSize = 7;
        for (int i = 0; i < input.length() / byteSize; i++) {
            int beginIndex = i * byteSize;
            int endIndex = beginIndex + 7;
            char c = (char) Integer.parseInt(input.substring(beginIndex, endIndex), 2);
            builder.append(c);
        }
        return builder.toString();
    }
}
