import java.util.*;

public class Cinema {
    public static void main(String[] args) {
        int rows = getInput("Enter the number of rows:");
        int columns = getInput("Enter the number of seats in each row:");
        System.out.println();

        char[][] seats = createSeats(rows, columns);

        boolean running = true;
        while (running) {
            int input = getInput("""
                    1. Show the seats
                    2. Buy a ticket
                    3. Statistics
                    0. Exit""");
            switch (input) {
                case 1:
                    showSeats(seats);
                    break;
                case 2:
                    buyTicket(seats);
                    break;
                case 3:
                    showStatistics(seats);
                    break;
                case 0:
                    running = false;
                    break;
            }
        }
    }

    public static char[][] createSeats(int rows, int columns) {
        char[][] seats = new char[rows][columns];
        for (int i = 0; i < seats.length; i++) {
            Arrays.fill(seats[i], 'S');
        }
        return seats;
    }

    public static int getInput(String message) {
        Scanner scanner = new Scanner(System.in);
        System.out.println(message);
        return scanner.nextInt();
    }

    public static int getRowSize(char[][] seats) {
        return seats == null ? 0 : seats.length;
    }

    public static int getColumnSize(char[][] seats) {
        return getRowSize(seats) > 0 ? seats[0].length : 0;
    }

    public static void showSeats(char[][] seats) {
        int rows = getRowSize(seats);
        int columns = getColumnSize(seats);
        System.out.println();
        System.out.println("Cinema:");
        for (int i = 0; i <= columns; i++) {
            if (i == 0) {
                System.out.print(" ");
            } else {
                System.out.print(" " + i);
            }
        }
        System.out.println();

        for (int i = 0; i < rows; i++) {
            System.out.print(i + 1);
            for (int j = 0; j < columns; j++) {
                System.out.print(" " + seats[i][j]);
            }
            System.out.println();
        }
        System.out.println();
    }

    public static void buyTicket(char[][] seats) {
        int rows = getRowSize(seats);
        int columns = getColumnSize(seats);
        int row;
        int column;

        System.out.println();
        while (true) {
            row = getInput("Enter a row number:");
            column = getInput("Enter a seat number in that row:");

            if (row < 1 || row > rows || column < 1 || column > columns) {
                System.out.println();
                System.out.println("Wrong input!");
                System.out.println();
                continue;
            }

            if (seats[row - 1][column - 1] == 'B') {
                System.out.println();
                System.out.println("That ticket has already been purchased!");
                System.out.println();
                continue;
            }

            break;
        }

        seats[row - 1][column - 1] = 'B';
        int price = calculateTicketPrice(row, column, rows, columns);
        System.out.println();
        System.out.println("Ticket price: $" + price);
        System.out.println();
    }

    public static int calculateTicketPrice(int row, int column, int rows, int columns) {
        int seatCount = rows * columns;
        if (seatCount < 60) {
            return 10;
        }

        int frontHalf = rows / 2;
        if (row <= frontHalf) {
            return 10;
        }

        return 8;
    }

    public static void showStatistics(char[][] seats) {
        int rows = getRowSize(seats);
        int columns = getColumnSize(seats);
        int seatCount = rows * columns;
        int purchasedTickets = countPurchasedTickets(seats);
        double percentage = (double) purchasedTickets / (double) seatCount * 100.0;

        System.out.println();
        System.out.printf("Number of purchased tickets: %d%n", purchasedTickets);
        System.out.printf("Percentage: %.2f%%%n", percentage);
        System.out.printf("Current income: $%d%n", calculateCurrentIncome(seats));
        System.out.printf("Total income: $%d%n", calculateTotalIncome(seats));
        System.out.println();
    }

    public static int countPurchasedTickets(char[][] seats) {
        int count = 0;
        int rows = getRowSize(seats);
        int columns = getColumnSize(seats);
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < columns; j++) {
                if (seats[i][j] == 'B') {
                    count++;
                }
            }
        }
        return count;
    }

    public static int calculateCurrentIncome(char[][] seats) {
        int income = 0;
        int rows = getRowSize(seats);
        int columns = getColumnSize(seats);
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < columns; j++) {
                if (seats[i][j] == 'B') {
                    income += calculateTicketPrice(i + 1, j + 1, rows, columns);
                }
            }
        }
        return income;
    }

    public static int calculateTotalIncome(char[][] seats) {
        int income = 0;
        int rows = getRowSize(seats);
        int columns = getColumnSize(seats);
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < columns; j++) {
                income += calculateTicketPrice(i + 1, j + 1, rows, columns);
            }
        }
        return income;
    }
}
