class AssetSimulator():
    """
    将来的な資産を予測する。

    Paremeters
    ------------
    start_salary: 初年度の年収
    max_salary: 年収の上限
    work_year: 働く年数
    increase_ammount: 毎年の昇給額
    savings_rate: 給与収入の貯蓄割合
    investment_yield: 資産運用の利回り
    start_asset: シミュレーション開始時の資産
    stock_option_rate: ストックオプションの割合
    stock_option_strike: ストックオプションの行使価格
    estimated_valuation: 推定企業価値
    """

    def __init__(self, start_salary, max_salary, work_year, increase_amount, saving_rate=0.15, investment_yield=0.03, start_asset=0, stock_option_rate=None, stock_option_strike=None, estimated_valuation=None):
        self.asset = start_asset
        self.salary = start_salary
        self.max_salary = max_salary
        self.work_year = work_year
        self.increase_amount = increase_amount
        self.saving_rate = saving_rate
        self.investment_yield = investment_yield
        self.year = 1
        self.stock_option_rate = stock_option_rate
        self.stock_option_strike = stock_option_strike
        self.estimated_valuation = estimated_valuation
        self.asset_list = self._predict()

    def get_asset(self):
        """
        シミュレートした累計資産のリストを返す。
        """
        return self.asset_list

    def _predict(self):
        """
        資産形成のシミュレーションを行う。
        """
        asset_list = [-1 for _ in range(self.work_year)]
        tmp_list = [0 for _ in range(self.work_year)]  # 給与収入のうちで資産運用しない分
        for i in range(self.work_year):
            # 給与収入の一部を資産運用
            self.asset += self._get_after_tax(self.salary) * self.saving_rate
            tmp_list[i] = self._get_after_tax(
                self.salary) * (1 - self.saving_rate) + tmp_list[i-1]  # 給与収入のうち資産運用しない分
            self.salary += self.increase_amount  # 昇給
            if self.salary > self.max_salary:
                self.salary = self.max_salary
            if i == 6 and self.stock_option_rate:  # 6年後にストックオプションの期待収入を受け取るとする。（近似）
                self.asset += (self.estimated_valuation * self.stock_option_rate -
                               self.stock_option_strike) * (1 - 0.2315)
            asset_list[i] = self.asset
            self.asset *= (1 + self.investment_yield)
        assert (-1 not in asset_list)
        assert 0 not in tmp_list
        self.tmp_list = tmp_list
        total_asset_list = [asset + tmp for asset,
                            tmp in zip(asset_list, tmp_list)]
        return total_asset_list

    def _get_after_tax(self, salary):
        """
        手取りを計算
        """
        income_tax = self._calc_progressive_tax(salary)  # 所得税
        resident_tax = self.salary * 0.7 * 0.1 + 4500  # 住民税(年収の30%をボーナスとする。)
        health_insurance_fee = self.salary * 0.05  # 保険料
        pension = self.salary * 0.0915  # 年金
        tax_sum = income_tax + resident_tax + health_insurance_fee + pension
        return self.salary - tax_sum

    def _calc_progressive_tax(self, salary):
        """
        所得税の計算
        """
        if salary <= 1950000:
            tax = salary * 0.05
        elif salary <= 3300000:
            tax = salary * 0.1 - 97500
        elif salary <= 6950000:
            tax = salary * 0.2 - 427500
        elif salary <= 9000000:
            tax = salary * 0.23 - 636000
        elif salary <= 18000000:
            tax = salary * 0.33 - 1536000
        elif salary <= 40000000:
            tax = salary * 0.4 - 2796000
        else:
            tax = salary * 0.45 - 4796000
        return tax