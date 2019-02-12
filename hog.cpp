#include "stdafx.h"
#include "hog.h"

// Implementation of game of hog 

// default dice
FairDice DEFAULT_DICE = FairDice(DICE_SIDES);

AlwaysRollStrategy * ALWAYS_ROLL_FOUR_STRATEGY = new AlwaysRollStrategy(4);
IStrategy& DEFAULT_STRATEGY = *ALWAYS_ROLL_FOUR_STRATEGY;

int enable_time_trot = true;
int enable_swine_swap = true;

int roll_dice(int num_rolls, IDice& dice) {
    bool found_one = false;
    int sum = 0;

    for (int i = 0; i < num_rolls; ++i) {
        int cur_roll = dice();

        if (cur_roll == 1)
            found_one = true;

        sum += cur_roll;

        if (found_one) return 1;
    }
		
    return sum;
}

int free_bacon(int score) {
    // SP19 rules
    return std::min((score / 10 % 10), score % 10) + 1;

    /*
    // FA18 rules
    return std::max(2 * (score / 10 % 10) - score % 10, 1);
    */

    /*
    // SP18 rules
    int max_digit = 0;

    while (score > 0) {
        max_digit = std::max(score % 10, max_digit);
        score /= 10;
    }
    return max_digit + 1;
    */
}

int take_turn(int num_rolls, int score1, IDice& dice){
    int delta = 0;
	
    if (num_rolls == 0){
        delta = free_bacon(score1);
    }
    else {
        delta = roll_dice(num_rolls, dice);
    }

    return delta;
}

int is_swap(int score0, int score1) {
    if (!enable_swine_swap) return false;
    // SP19 rules
    for (; score0 && score1; score0 /= 10, score1 /= 10) {
        if (score0 % 10 == score1 % 10) {
            return 1;
        }
    }
    return 0;
    
    /*
    // FA18 rules
    return abs(score0 / 10 % 10 - score0 % 10) == abs(score1 / 10 % 10 - score1 % 10);
    */
    /*
    // SP18 rules
    if (score0 <= 1 || score1 <= 1) return false;
    return score0 % score1 == 0 || score1 % score0 == 0;
    */
}

int is_time_trot(int turn_num, int rolls) {
    if (!enable_time_trot) return false;
    return turn_num % MOD_TROT == rolls;
}

std::pair<int, int> play(IStrategy& strategy0, IStrategy& strategy1, int score0, int score1, 
                    IDice& dice, int goal, int starting_turn) {

    int player = 0, turn_num = starting_turn;
    bool last_time_trot = false; // prevents multiple time trot in a row

    while (score0 < goal && score1 < goal) {
        int rolls = 0;

        if (player == 0) {
            rolls = strategy0(score0, score1);
            score0 += take_turn(rolls, score1, dice);
        }
        else {
            rolls = strategy1(score1, score0);
            score1 += take_turn(rolls, score0, dice);
        }

        if (is_swap(score0, score1)) {
            std::swap(score0, score1);
        }

        if (is_time_trot(turn_num, rolls) && ! last_time_trot) { // implementation of time trot
            last_time_trot = true; // don't switch player
        }
        else {
            player = 1 - player; // switch player
            last_time_trot = false;
        }

        ++turn_num;
    }

    return std::pair<int, int>(score0, score1);
}
