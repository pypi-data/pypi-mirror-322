import unittest
import time

from parametric_ttl_cache.ttl_cache import TtlCache


class TestTtlCache(unittest.TestCase):
    __increment = 0
    def test_ttl_cache(self):
        ttl = 2  # 2 seconds
        cache = TtlCache(ttl)

        def incrementer():
            self.__increment += 1
            return self.__increment

        @cache
        def func(x=1):
            return x + incrementer()

        self.assertEqual(func(1), 2, '첫 번 째 호출은 정상적으로 실행')
        self.assertEqual(func(1), 2, '두 번 째 호출은 캐시에서 가져와야 하고 incrementer가 호출되지 않아야 함')
        self.assertEqual(func(x=1), 2, '명시적인 키워드 인자도 동일한 캐시 키로 사용되어야 함')
        self.assertEqual(func(), 2, '디폴트 인자와 캐시 키로 사용된 인자가 같으면 같은 캐시 키로 취급되어야 함')
        self.assertEqual(func(2), 4, '인자가 다르면 다른 캐시가 생성되어야 함')

        # 캐시 expire
        time.sleep(ttl + 1)

        self.assertEqual(func(1), 4, '캐시가 expire 되었으므로 incrementer가 호출되어야 함')
        self.assertEqual(func(1), 4, '이 전 호출에서 캐시가 다시 생성되어야 함')

        # 캐시 강제 expire
        cache.force_expire('x=1')

        self.assertEqual(func(1), 5, '강제로 캐시를 expire시키면 incrementer가 호출되어야 함')


if __name__ == '__main__':
    unittest.main()
