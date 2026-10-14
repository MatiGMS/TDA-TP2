import unittest

from tp2_2 import main, actualizar_servidor

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

        posible2, flujo_max2, _ = actualizar_servidor("S2", 4)

        self.assertFalse(posible2)
        self.assertEqual(flujo_max2, 9)

if __name__ == "__main__":
    unittest.main()
