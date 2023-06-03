import java.io.File;
import java.io.FileNotFoundException;
import java.util.Random;
import java.util.Scanner;

public class RockPaperScissors {
    enum ResultType {
        DRAW, PLAYER1, PLAYER2
    }

    private static String[] inputOptions;

    public static void main(String[] args) {
        String playerName = getInput("Enter your name: ");
        int playerScore = getPlayerScore(playerName);
        System.out.printf("Hello, %s%n", playerName);
        loadInputOptions();
        System.out.println("Okay, let's start");

        boolean running = true;
        while (running) {
            String playerInput = getPlayerInput();
            String computerInput = getComputerInput();

            if (hasOptionInOptions(playerInput)) {
                showResults(playerInput, computerInput);
                playerScore += getScoreForMatch(playerInput, computerInput);
                continue;
            }

            switch (playerInput) {
                case "!rating":
                    System.out.printf("Your rating: %d%n", playerScore);
                    break;
                case "!exit":
                    System.out.println("Bye!");
                    running = false;
                    break;
                default:
                    System.out.println("Invalid input");
                    break;
            }
        }
    }

    private static void showResults(String playerInput, String computerInput) {
        ResultType result = getResult(playerInput, computerInput);
        switch (result) {
            case DRAW:
                System.out.printf("There is a draw (%s)%n", playerInput);
                break;
            case PLAYER1:
                System.out.printf("Well done. The computer chose %s and failed%n", computerInput);
                break;
            case PLAYER2:
                System.out.printf("Sorry, but the computer chose %s%n", computerInput);
                break;
        }
    }

    private static ResultType getResult(String player1, String player2) {
        if (player1.equals(player2)) {
            return ResultType.DRAW;
        }

        String[] relations = new String[inputOptions.length - 1];
        int player1Index = getIndexOfOption(player1);

        int j = (player1Index + 1) % inputOptions.length;
        for (int i = 0; i < relations.length; i++) {
            relations[i] = inputOptions[j];
            j = (j + 1) % inputOptions.length;
        }

        int player2Index = getIndexOfOption(player2, relations);
        int center = (int) relations.length / 2;
        if (player2Index < center) {
            return ResultType.PLAYER1;
        } else {
            return ResultType.PLAYER2;
        }
    }

    private static int getScoreForMatch(String player1, String player2) {
        ResultType result = getResult(player1, player2);
        switch (result) {
            case DRAW:
                return 50;
            case PLAYER1:
                return 100;
        }
        return 0;
    }

    private static String getInput() {
        return getInput("");
    }

    private static String getInput(String message) {
        Scanner scanner = new Scanner(System.in);
        System.out.printf(message);
        return scanner.nextLine();
    }

    private static String getPlayerInput() {
        String input = getInput();
        return input.toLowerCase().trim();
    }

    private static int getPlayerScore(String player) {
        try (Scanner scanner = new Scanner(new File("./rating.txt"))) {
            while (scanner.hasNextLine()) {
                String[] parts = scanner.nextLine().split(" ");
                String name = parts[0];
                int score = Integer.parseInt(parts[1]);
                if (name.equals(player)) {
                    return score;
                }
            }
        } catch (FileNotFoundException e) {
        }
        return 0;
    }

    private static String getComputerInput() {
        String[] choices = {"rock", "paper", "scissors"};
        Random rng = new Random();
        int choice = rng.nextInt(choices.length);
        return choices[choice];
    }

    private static void loadInputOptions() {
        String input = getInput().trim().toLowerCase();
        if (input.isEmpty()) {
            input = "rock,paper,scissors";
        }
        inputOptions = input.split(",");
    }

    private static int getIndexOfOption(String option, String[] options) {
        for (int i = 0; i < options.length; i++) {
            if (option.equals(options[i])) {
                return i;
            }
        }
        return -1;
    }

    private static int getIndexOfOption(String option) {
        return getIndexOfOption(option, inputOptions);
    }

    private static boolean hasOptionInOptions(String option) {
        int index = getIndexOfOption(option);
        return index != -1;
    }
}
