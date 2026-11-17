class Plane:
    def __init__(self, length):
        self.length = length
        self.seats = [[[] for _ in range(length + 2)] for _ in range(7)]

    def add_passengers(self, psg_list):
        for psg in psg_list:
            psg.add_to_plane(self)
            self.seats[3][0].append(psg)

    def is_empty(self, row, seat):
        if not (0 <= seat < 7 and 0 <= row < self.length + 2):
            return True
        return len(self.seats[seat][row]) == 0

    def move_row(self, row, seat_letter):
        if self.is_empty(row + 1, 3):
            target_map = {'F': 0, 'E': 1, 'D': 2, 'C': 4, 'B': 5, 'A': 6}
            target_idx = target_map[seat_letter]
            step = 1 if target_idx > 3 else -1
            
            for s in range(3 + step, target_idx + step, step):
                for p in self.seats[s][row]:
                    p.forced_to_move(3, row + 1)
                    self.seats[3][row + 1].append(p)
                self.seats[s][row] = []

    def return_row(self, row):
        waiting = self.seats[3][row + 1][:]
        for p in waiting:
            s_idx, r_idx = p.get_seat()
            if r_idx == row:
                p.forced_to_move(s_idx, r_idx)
                self.seats[s_idx][r_idx].append(p)
                self.seats[3][row + 1].remove(p)

    def move_passengers(self):
        to_move = []
        for s in range(7):
            for r in range(self.length + 2):
                for p in self.seats[s][r]:
                    to_move.append((p, s, r))

        for p, old_s, old_r in to_move:
            old_pos = p.get_position()
            new_pos = p.move()
            
            if old_pos != new_pos:
                new_r, new_s = new_pos
                if p in self.seats[old_s][old_r]:
                    self.seats[old_s][old_r].remove(p)
                    self.seats[new_s][new_r].append(p)

    def boarding_finished(self):
        for r in range(self.length + 2):
            if not self.is_empty(r, 3):
                return False
        
        count = 0
        for r in range(1, self.length + 1):
            for s in [0, 1, 2, 4, 5, 6]:
                if not self.is_empty(r, s):
                    count += 1
        return count == self.length * 6