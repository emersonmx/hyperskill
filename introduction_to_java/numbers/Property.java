package numbers;

import java.util.Arrays;

enum Property {
    BUZZ, DUCK, PALINDROMIC, GAPFUL, SPY, SQUARE, SUNNY, JUMPING, HAPPY, SAD, EVEN, ODD;

    public static boolean has(String property) {
        for (Property p : values()) {
            if (p.toString().equals(property)) {
                return true;
            }
        }
        return false;
    }
}