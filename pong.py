import arcade

# Constants for screen dimensions and game elements
SCREEN_WIDTH    = 800
SCREEN_HEIGHT   = 600
SCREEN_TITLE    = "Classic Pong Game"
PADDLE_WIDTH    = 10
PADDLE_HEIGHT   = 100
BALL_RADIUS     = 10
PADDLE_SPEED    = 5

# Ball speed options for difficulty levels
BALL_SPEEDS = {
    "easy":     (3, 3),
    "medium":   (5, 5),
    "hard":     (7, 7)
}

class PongGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        # Initialize paddles
        self.paddle1_y = SCREEN_HEIGHT // 2
        self.paddle2_y = SCREEN_HEIGHT // 2
        
        # Initialize ball
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_dx = 0
        self.ball_dy = 0
        
        # Initialize scores
        self.score1 = 0
        self.score2 = 0
        
        # Keep track of key states
        self.key_state = {
            "w":    False,     # Player 1 Up
            "s":    False,     # Player 1 Down
            "up":   False,    # Player 2 Up
            "down": False   # Player 2 Down
        }
        
        # Game state: "menu", "gameplay", or "game_over"
        self.game_state = "menu"
        self.selected_difficulty = None
        self.winner = None  # To store the winner's name
        
        # Set background color
        arcade.set_background_color(arcade.color.BLACK)
    
    def on_draw(self):
        """Render the screen."""
        arcade.start_render()
        
        if self.game_state == "menu":
            # Draw menu
            arcade.draw_text("Classic Pong", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100,
                             arcade.color.WHITE, 50, anchor_x="center")
            arcade.draw_text("Select Difficulty:", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                             arcade.color.WHITE, 30, anchor_x="center")
            arcade.draw_text("1. Easy", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                             arcade.color.GREEN, 25, anchor_x="center")
            arcade.draw_text("2. Medium", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                             arcade.color.YELLOW, 25, anchor_x="center")
            arcade.draw_text("3. Hard", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100,
                             arcade.color.RED, 25, anchor_x="center")
        
        elif self.game_state == "gameplay":
            # Draw paddles
            arcade.draw_rectangle_filled(20, self.paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT, arcade.color.WHITE)
            arcade.draw_rectangle_filled(SCREEN_WIDTH - 20, self.paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT, arcade.color.WHITE)
            
            # Draw ball
            arcade.draw_circle_filled(self.ball_x, self.ball_y, BALL_RADIUS, arcade.color.WHITE)
            
            # Draw divider
            arcade.draw_line(SCREEN_WIDTH // 2, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT, arcade.color.WHITE, 2)
            
            # Draw scores
            arcade.draw_text(f"{self.score1}", SCREEN_WIDTH // 4, SCREEN_HEIGHT - 50, arcade.color.WHITE, 36, anchor_x="center")
            arcade.draw_text(f"{self.score2}", SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT - 50, arcade.color.WHITE, 36, anchor_x="center")
        
        elif self.game_state == "game_over":
            # Display winner message
            arcade.draw_text(f"{self.winner} Wins!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                             arcade.color.WHITE, 50, anchor_x="center")
            arcade.draw_text("Press R to Return to Menu", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 75,
                             arcade.color.GRAY, 25, anchor_x="center")
    
    def on_update(self, delta_time):
        """Update the game state."""
        if self.game_state == "gameplay":
            # Move paddles based on key states
            if self.key_state["w"] and self.paddle1_y + PADDLE_HEIGHT // 2 < SCREEN_HEIGHT:
                self.paddle1_y += PADDLE_SPEED
            if self.key_state["s"] and self.paddle1_y - PADDLE_HEIGHT // 2 > 0:
                self.paddle1_y -= PADDLE_SPEED
            
            if self.key_state["up"] and self.paddle2_y + PADDLE_HEIGHT // 2 < SCREEN_HEIGHT:
                self.paddle2_y += PADDLE_SPEED
            if self.key_state["down"] and self.paddle2_y - PADDLE_HEIGHT // 2 > 0:
                self.paddle2_y -= PADDLE_SPEED
            
            # Move ball
            self.ball_x += self.ball_dx
            self.ball_y += self.ball_dy
            
            # Ball collision with top and bottom
            if self.ball_y <= BALL_RADIUS or self.ball_y >= SCREEN_HEIGHT - BALL_RADIUS:
                self.ball_dy *= -1
            
            # Ball collision with paddles
            if (self.ball_x - BALL_RADIUS <= 30 and abs(self.ball_y - self.paddle1_y) <= PADDLE_HEIGHT // 2):
            # Ball is hitting paddle1, reverse the horizontal direction
                self.ball_dx *= -1
                # Ensure the ball's vertical direction is adjusted based on where it hits the paddle
                if self.ball_y < self.paddle1_y - PADDLE_HEIGHT // 4:
                    self.ball_dy = -abs(self.ball_dy)  # Hit the top part of the paddle
                elif self.ball_y > self.paddle1_y + PADDLE_HEIGHT // 4:
                    self.ball_dy = abs(self.ball_dy)   # Hit the bottom part of the paddle
            
            if (self.ball_x + BALL_RADIUS >= SCREEN_WIDTH - 30 and abs(self.ball_y - self.paddle2_y) <= PADDLE_HEIGHT // 2):
                # Ball is hitting paddle2, reverse the horizontal direction
                self.ball_dx *= -1
                # Ensure the ball's vertical direction is adjusted based on where it hits the paddle
                if self.ball_y < self.paddle2_y - PADDLE_HEIGHT // 4:
                    self.ball_dy = -abs(self.ball_dy)  # Hit the top part of the paddle
                elif self.ball_y > self.paddle2_y + PADDLE_HEIGHT // 4:
                    self.ball_dy = abs(self.ball_dy)   # Hit the bottom part of the paddle
            
            # Ball goes out of bounds (player scores)
            if self.ball_x < 0:
                self.score2 += 1
                self.reset_ball()
            elif self.ball_x > SCREEN_WIDTH:
                self.score1 += 1
                self.reset_ball()
            
            # Check for a winner
            if self.score1 >= 10:
                self.game_state = "game_over"
                self.winner = "Player One"
            elif self.score2 >= 10:
                self.game_state = "game_over"
                self.winner = "Player Two"
    
    def reset_ball(self):
        """Reset ball to the center after a score."""
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_dx *= -1  # Send ball towards scoring player

    def set_difficulty(self, difficulty):
        """Set the game difficulty and start the game."""
        self.selected_difficulty = difficulty
        self.ball_dx, self.ball_dy = BALL_SPEEDS[difficulty]
        self.score1 = 0
        self.score2 = 0
        self.game_state = "gameplay"
    
    def on_key_press(self, key, modifiers):
        """Handle key press to move paddles or select difficulty."""
        if self.game_state == "menu":
            if key == arcade.key.KEY_1:
                self.set_difficulty("easy")
            elif key == arcade.key.KEY_2:
                self.set_difficulty("medium")
            elif key == arcade.key.KEY_3:
                self.set_difficulty("hard")
        elif self.game_state == "gameplay":
            if key == arcade.key.W:
                self.key_state["w"] = True
            elif key == arcade.key.S:
                self.key_state["s"] = True
            if key == arcade.key.UP:
                self.key_state["up"] = True
            elif key == arcade.key.DOWN:
                self.key_state["down"] = True
        elif self.game_state == "game_over":
            if key == arcade.key.R:
                self.game_state = "menu"
    
    def on_key_release(self, key, modifiers):
        """Handle key release to stop paddles."""
        if key == arcade.key.W:
            self.key_state["w"] = False
        elif key == arcade.key.S:
            self.key_state["s"] = False
        if key == arcade.key.UP:
            self.key_state["up"] = False
        elif key == arcade.key.DOWN:
            self.key_state["down"] = False

def main():
    game = PongGame()
    arcade.run()

if __name__ == "__main__":
    main()
