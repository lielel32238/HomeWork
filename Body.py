class Body:
    def __init__(self, mass, specific_heat, temperature):
        if mass <= 0:
            raise ValueError("Mass must be greater than 0")
        if specific_heat <= 0:
            raise ValueError("Specific heat must be greater than 0")
        if temperature < 0:
            raise ValueError("Temperature must be 0 or higher")
            
        self.mass = mass
        self.specific_heat = specific_heat
        self.temperature = temperature

    def add_heat(self, q):
        delta_t = q / (self.mass * self.specific_heat)
        self.temperature += delta_t
        return self.temperature

if __name__ == "__main__":
    b = Body(100, 0.15, 200)
    print(b.add_heat(20))   
    print(b.add_heat(-40)) 
