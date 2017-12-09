import Commans
from runs.IRun import IRun
from dbs.MysqlC import MysqlC
from rules2.DB_VarcharRule import VarcharRule

class DBRun(IRun):
    def __init__(self,DB):
        super().__init__(DB)

        self._params = {}
    def addTaskParams(self,tbl):
        self._params = {'tbl':tbl}
    def run(self):
        self._fields = tuple(self._rules)
        try:
            print(self._rules)
            values = tuple(self._rules[v].getValue() for v in self._fields)
            params = {
                'table': self._params['tbl'],
                'binds': values,
                'field': self._fields
            }
            # print(params)
            if not self._operator.add(params):
                self._setError(self._operator.getError())
            # print(self._params['tbl']);

        except Exception as E:
            self._setError(str(E))
            print('DB Run 38')
            print(E)
        pass

if __name__ == '__main__':
    # c=Commans.Comman()
    # c.getConfig()
    RUN = DBRun(MysqlC())
    varOBJ = VarcharRule({"end": 1000, "step": 2, "start": 1, "prefix": "XXX"})
    RUN.addTaskParams('liv_dog_info')
    RUN.addTask('context',varOBJ)
    RUN.run()
    # {"context": {"end": 1000, "step": 2, "start": 1, "prefix": "XXX"}}
