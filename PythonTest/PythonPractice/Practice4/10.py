for A in range(1, 10):
    for B in range(0, 10):
        for C in range(1, 10):
            for D in range(0, 10):
                ABCD = A * 1000 + B * 100 + C * 10 + D
                CDC = C * 100 + D * 10 + C
                ABC = A * 100 + B * 10 + C
                if ABCD - CDC == ABC:
                    print(f"A={A} B={B} C={C} D={D}")
