package numbers;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

class ANumber {
    private long value;

    public ANumber(long value) {
        assert value > 0;
        this.value = value;
    }

    public ANumber(String value) {
        this(Long.parseLong(value));
    }

    public long getValue() {
        return value;
    }

    public boolean isEven() {
        return value % 2 == 0;
    }

    public boolean isOdd() {
        return value % 2 == 1;
    }

    public boolean isBuzz() {
        boolean endWithSeven = value % 10 == 7;
        boolean isDivisibleBySeven = value % 7 == 0;
        return endWithSeven || isDivisibleBySeven;
    }

    public boolean isDuck() {
        return String.valueOf(value).indexOf("0") != -1;
    }

    public boolean isPalindromic() {
        String number = String.valueOf(value);
        StringBuilder builder = new StringBuilder(number);
        return builder.reverse().toString().equals(number);
    }

    public boolean isGapful() {
        Pattern pattern = Pattern.compile("(\\d)(\\d+)(\\d)");
        Matcher matcher = pattern.matcher(String.valueOf(value));
        if (!matcher.matches()) {
            return false;
        }

        long modNumber = Long.parseLong(matcher.group(1) + matcher.group(3));
        long number = Long.parseLong(matcher.group(0));
        return number % modNumber == 0;
    }

    public boolean isSpy() {
        char[] numbers = String.valueOf(value).toCharArray();

        long sum = 0;
        long product = 1;
        for (int i = 0; i < numbers.length; i++) {
            long number = Long.parseLong(String.valueOf(numbers[i]));
            sum += number;
            product *= number;
        }

        return sum == product;
    }

    public boolean isSquare() {
        return isSquare(value);
    }

    private boolean isSquare(double value) {
        double result = Math.sqrt(value);
        double floorResult = Math.floor(result);
        return result == floorResult;
    }

    public boolean isSunny() {
        return isSquare(value + 1);
    }

    public boolean isJumping() {
        char[] digits = String.valueOf(this.value).toCharArray();
        boolean result = true;
        for (int i = 1; i < digits.length; i++) {
            int last = digits[i - 1] - '0';
            int current = digits[i] - '0';
            int diff = Math.abs(current - last);
            result = result && diff == 1;
        }
        return result;
    }

    public boolean isHappy() {
        long sum = 0;
        long number = this.value;
        int count = 0;
        while (sum != 1) {
            if (number == 4) {
                return false;
            }
            sum = 0;
            while (number > 0) {
                long digit = number % 10;
                sum += digit * digit;
                number /= 10;
            }
            number = sum;
            count++;
        }
        return true;
    }

    public boolean isSad() {
        return !isHappy();
    }
}
