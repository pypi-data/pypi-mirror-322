from ray import init
from model_desc import model_desc, dir_to_desc_map
from actor_engine import ActorEngine
from engine_proxy import EngineProxy


class Aircraft:
    def __init__(self, desc_map: dict[str, model_desc]):
        # assume in the node where excute the code has ray cluste running
        init(address="auto")

        self.desc_map = desc_map

    @staticmethod
    def of(dir):
        desc_map = dir_to_desc_map(dir)
        return Aircraft(desc_map)

    def ls(self):
        l = list(self.desc_map.keys())
        l.sort()
        return l

    def takeoff(self, model_name):
        desc = self.desc_map[model_name]
        path = desc.path
        id = desc.platform_id
        with open(path, "rb") as f:
            data = f.read()
        e = ActorEngine.remote(data, id)
        return EngineProxy(e)
