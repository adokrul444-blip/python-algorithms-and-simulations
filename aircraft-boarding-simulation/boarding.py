import random
from passenger import Passenger
from plane import Plane

class Boarding:
    def __init__(self):
        self.plane = None

    def generate_boarding(self, plane_length):
        # Tato metoda bude implementovana v podtriedach
        pass

    def run_simulation(self, plane_length):
        boarding_list = self.generate_boarding(plane_length)
        # Lietadlo uz bolo vytvorene v generate_boarding, takze ho netreba prepisovat
        steps = 0
        while not self.plane.boarding_finished():
            if boarding_list:
                p = boarding_list.pop(0)
                # Pasažiera netreba znova pridavat do seats[3][0], 
                # pretoze tam uz je z generate_boarding.
                # Ale musime ho nechat pohnut sa, ak uz nie je v zozname na cakacej listine.
                pass 
            self.plane.move_passengers()
            steps += 1
            if steps > 30000: break
        return steps

    def test_boarding_method(self, plane_length, no_simulation):
        results = [self.run_simulation(plane_length) for _ in range(no_simulation)]
        return sum(results) / no_simulation, results

class BoardingBTF(Boarding):
    def generate_boarding(self, plane_length):
        self.plane = Plane(plane_length)
        psgs = []
        for r in range(plane_length, 0, -2):
            batch = []
            for row in range(r, r - 2, -1):
                if row > 0:
                    batch.extend([Passenger(row, s, random.randint(0, 3)) for s in 'ABCDEF'])
            random.shuffle(batch)
            psgs.extend(batch)
        self.plane.add_passengers(psgs)
        return psgs

class BoardingFTB(Boarding):
    def generate_boarding(self, plane_length):
        self.plane = Plane(plane_length)
        psgs = []
        for r in range(1, plane_length + 1, 2):
            batch = []
            for row in range(r, r + 2):
                if row <= plane_length:
                    batch.extend([Passenger(row, s, random.randint(0, 3)) for s in 'ABCDEF'])
            random.shuffle(batch)
            psgs.extend(batch)
        self.plane.add_passengers(psgs)
        return psgs

class BoardingWTA(Boarding):
    def generate_boarding(self, plane_length):
        self.plane = Plane(plane_length)
        psgs = []
        for group in [('A', 'F'), ('B', 'E'), ('C', 'D')]:
            batch = [Passenger(r, s, random.randint(0, 3)) for r in range(1, plane_length + 1) for s in group]
            random.shuffle(batch)
            psgs.extend(batch)
        self.plane.add_passengers(psgs)
        return psgs

class BoardingATW(Boarding):
    def generate_boarding(self, plane_length):
        self.plane = Plane(plane_length)
        psgs = []
        for group in [('C', 'D'), ('B', 'E'), ('A', 'F')]:
            batch = [Passenger(r, s, random.randint(0, 3)) for r in range(1, plane_length + 1) for s in group]
            random.shuffle(batch)
            psgs.extend(batch)
        self.plane.add_passengers(psgs)
        return psgs

class BoardingRandom(Boarding):
    def generate_boarding(self, plane_length):
        self.plane = Plane(plane_length)
        psgs = [Passenger(r, s, random.randint(0, 3)) for r in range(1, plane_length + 1) for s in 'ABCDEF']
        random.shuffle(psgs)
        self.plane.add_passengers(psgs)
        return psgs

class BoardingSteffen(Boarding):
    def generate_boarding(self, plane_length):
        self.plane = Plane(plane_length)
        psgs = []
        seat_pairs = [('A', 'F'), ('B', 'E'), ('C', 'D')]
        
        for s1, s2 in seat_pairs:
            for s in [s1, s2]:
                for r in range(plane_length, 0, -2):
                    psgs.append(Passenger(r, s, random.randint(0, 3)))
            for s in [s1, s2]:
                for r in range(plane_length - 1, 0, -2):
                    psgs.append(Passenger(r, s, random.randint(0, 3)))
        
        self.plane.seats[3][0] = []
        self.plane.add_passengers(psgs)
        
        return psgs