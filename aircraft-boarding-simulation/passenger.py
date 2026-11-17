class Passenger:
    def __init__(self, row, seat, no_of_bags):
        if seat not in ['A', 'B', 'C', 'D', 'E', 'F']:
            raise ValueError("Seat must be a letter from A to F")

        self.row = row
        self.seat = seat
        self.bags = no_of_bags * 4

        self.plane = None
        self.current_position = [None, None]

    def __str__(self):
        return "<Passenger in seat: {}{}>".format(self.row, self.seat)

    def get_position(self):
        if self.current_position[0] is None:
            return None
        return self.current_position[1], self.current_position[0]

    def get_seat(self):
        seat_map = {'F': 0, 'E': 1, 'D': 2, 'C': 4, 'B': 5, 'A': 6}
        return seat_map[self.seat], self.row

    def add_to_plane(self, plane):
        self.plane = plane
        self.current_position = [0, 3]

    def forced_to_move(self, x, y):
        self.current_position = [y, x]

    def can_sit(self):
        if self.current_position[0] is None or self.current_position[1] != 3:
            return False
        
        if self.current_position[0] != self.row:
            return False

        if self.seat in ['C', 'D']:
            return True

        target_seat_idx, _ = self.get_seat()
        step = 1 if target_seat_idx > 3 else -1
        for s in range(3 + step, target_seat_idx, step):
            if not self.plane.is_empty(self.row, s):
                return False
        return True

    def move(self):
        if self.current_position[0] is None:
            raise ValueError("Passenger not in plane")

        curr_row, curr_col = self.current_position

        if curr_row < self.row:
            if self.plane.is_empty(curr_row + 1, 3):
                self.current_position[0] += 1
            return self.current_position[0], self.current_position[1]

        if self.bags > 0:
            self.bags -= 1
            return self.current_position[0], self.current_position[1]

        if curr_col == 3:
            if self.can_sit():
                target_seat, _ = self.get_seat()
                self.current_position = [self.row, target_seat]
                self.plane.return_row(self.row)
            else:
                self.plane.move_row(self.row, self.seat)
        
        return self.current_position[0], self.current_position[1]