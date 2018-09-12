import unittest
import numpy as np
import pandas as pd

from toad.utils import clip, diff_time_frame, bin_to_number

np.random.seed(1)
feature = np.random.rand(500)
target = np.random.randint(2, size = 500)

class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_clip(self):
        res1 = clip(feature, quantile = (.05, .95))
        res2 = clip(feature, quantile = 0.05)
        self.assertIsNone(np.testing.assert_array_equal(res1, res2))

    def test_diff_time_frame(self):
        time_data = [
            {
                'base': '2018-01',
                'time1': '2018-04',
                'time2': '2018-04-02',
            },
            {
                'base': '2018-01',
                'time1': '2018-05',
                'time2': '2018-04-05',
            },
            {
                'base': '2018-02',
                'time1': '2018-04',
                'time2': '2018-04-10',
            },
        ]

        frame = pd.DataFrame(time_data)
        res = diff_time_frame(frame['base'], frame[['time1', 'time2']], format='%Y-%m-%d')
        self.assertEqual(res.iloc[0, 1], 91)

    def test_bin_to_number(self):
        s = pd.Series([
            '1',
            '1-100',
            '-',
            '100-200',
            np.nan,
            '200-300',
            '300',
            '100-200',
            '>500',
        ])

        res = s.apply(bin_to_number())
        self.assertEqual(res[3], 150)

    def test_bin_to_number_for_frame(self):
        df = pd.DataFrame([
            {
                'area_1': '100-200',
                'area_2': '150~200',
            },
            {
                'area_1': '300-400',
                'area_2': '200~250',
            },
            {
                'area_1': '200-300',
                'area_2': '450~500',
            },
            {
                'area_1': '100-200',
                'area_2': '250~300',
            },
        ])

        res = df.applymap(bin_to_number())
        self.assertEqual(res.loc[1, 'area_2'], 225)