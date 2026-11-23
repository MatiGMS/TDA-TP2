import unittest

from tp2_2 import actualizar_servidor, main


class TestFestivalParteA(unittest.TestCase):
    def test_ejemplo_del_enunciado_factible(self):
        bandas = [("B1", 6), ("B2", 4)]
        servidores = [("S1", 5), ("S2", 6)]
        plataformas = [("P1", 5), ("P2", 5)]
        bs = [("B1", "S1"), ("B1", "S2"), ("B2", "S2")]
        sp = [("S1", "P1"), ("S2", "P1"), ("S2", "P2")]

        posible, flujo_max, asignacion = main(bandas, servidores, plataformas, bs, sp)

        self.assertTrue(posible)
        self.assertEqual(flujo_max, 10)
        self.assertEqual(sum(cant for _, _, cant in asignacion), 10)

    def test_correccion_parte_a(self):
        bandas = [("B0", 1), ("B1", 3)]
        servidores = [("S0", 6), ("S1", 3)]
        plataformas = [("P0", 2), ("P1", 2), ("P2", 5)]
        bs = [("B0", "S0"), ("B1", "S0")]
        sp = [("S0", "P1"), ("S0", "P2"), ("S1", "P1")]

        posible, flujo_max, asignacion = main(bandas, servidores, plataformas, bs, sp)

        self.assertTrue(posible)
        self.assertEqual(flujo_max, 4)
        por_banda = {}
        for b, _, cant in asignacion:
            por_banda[b] = por_banda.get(b, 0) + cant
        self.assertEqual(por_banda, {"B0": 1, "B1": 3})


class TestFestivalParteB(unittest.TestCase):
    def test_disminuir_servidor_vuelve_infactible(self):
        bandas = [("B1", 6), ("B2", 4)]
        servidores = [("S1", 5), ("S2", 6)]
        plataformas = [("P1", 5), ("P2", 5)]
        bs = [("B1", "S1"), ("B1", "S2"), ("B2", "S2")]
        sp = [("S1", "P1"), ("S2", "P1"), ("S2", "P2")]

        posible, flujo_max, _ = main(bandas, servidores, plataformas, bs, sp)
        self.assertTrue(posible)
        self.assertEqual(flujo_max, 10)

        posible2, flujo_max2, asignacion2 = actualizar_servidor("S2", 4)

        self.assertFalse(posible2)
        self.assertEqual(flujo_max2, 9)
        self.assertEqual(sum(cant for _, _, cant in asignacion2), 9)

    def test_correccion_parte_b_aumento(self):
        bandas = [("B1", 1), ("B2", 5)]
        servidores = [("S1", 3), ("S2", 2)]
        plataformas = [("P1", 4), ("P2", 4), ("P3", 4)]
        bs = [("B1", "S2"), ("B2", "S1"), ("B2", "S2")]
        sp = [
            ("S1", "P1"), ("S1", "P2"), ("S1", "P3"),
            ("S2", "P1"), ("S2", "P2"), ("S2", "P3"),
        ]

        posible, flujo_max, _ = main(bandas, servidores, plataformas, bs, sp)
        self.assertFalse(posible)
        self.assertEqual(flujo_max, 5)

        posible2, flujo_max2, asignacion2 = actualizar_servidor("S1", 6)

        self.assertTrue(posible2)
        self.assertEqual(flujo_max2, 6)
        self.assertEqual(sum(cant for _, _, cant in asignacion2), 6)

    def test_disminuir_servidor_multipasada(self):
        bandas = [("B1", 6), ("B2", 4)]
        servidores = [("S1", 5), ("S2", 6)]
        plataformas = [("P1", 5), ("P2", 5)]
        bs = [("B1", "S1"), ("B1", "S2"), ("B2", "S2")]
        sp = [("S1", "P1"), ("S2", "P1"), ("S2", "P2")]

        main(bandas, servidores, plataformas, bs, sp)
        posible2, flujo_max2, asignacion2 = actualizar_servidor("S2", 2)

        self.assertFalse(posible2)
        self.assertEqual(flujo_max2, 7)
        self.assertEqual(sum(cant for _, _, cant in asignacion2), 7)


if __name__ == "__main__":
    unittest.main()
