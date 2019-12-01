def fuel(mass):
    return int(mass / 3) - 2


def recursive_fuel(initial_fuel):
    additional_fuel = 0
    extra = fuel(initial_fuel)
    while extra > 0:
        additional_fuel += extra
        extra = fuel(extra)
    return initial_fuel + additional_fuel


with open('data.txt') as file:
    modules = [
        int(line)
        for line in file
    ]

print('initial fuel: ',
      sum([
          fuel(module)
          for module in modules
      ])
      )

print('total fuel: ',
      sum([
          recursive_fuel(fuel(module))
          for module in modules
      ])
      )
