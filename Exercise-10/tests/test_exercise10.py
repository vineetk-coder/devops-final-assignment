"""Tests for Exercise-10: both Flask apps + all Kubernetes manifests."""
import importlib
import pathlib
import sys
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent  # Exercise-10/
sys.path.insert(0, str(ROOT))


class TestProductCatalog(unittest.TestCase):
    def test_products(self):
        app = importlib.import_module("product_catalog").app
        self.assertEqual(app.test_client().get("/products").get_json(), [
            {"id": 1, "name": "Laptop", "price": 1200},
            {"id": 2, "name": "Phone", "price": 800},
            {"id": 3, "name": "Headphones", "price": 150},
        ])


class TestShoppingCart(unittest.TestCase):
    def test_cart_flow(self):
        mod = importlib.import_module("shopping_cart")
        mod.cart.clear()
        c = mod.app.test_client()
        self.assertEqual(c.get("/cart").get_json(), [])
        item = {"id": 1, "name": "Laptop", "quantity": 1}
        r = c.post("/cart", json=item)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.get_json(), [item])
        self.assertEqual(c.get("/cart").get_json(), [item])


class TestManifests(unittest.TestCase):
    def load(self, name):
        return yaml.safe_load((ROOT / "k8s" / name).read_text())

    def check_deploy(self, name, app, replicas):
        d = self.load(name)
        self.assertEqual(d["metadata"]["namespace"], "default")
        self.assertEqual(d["spec"]["replicas"], replicas)
        spec = d["spec"]["template"]["spec"]
        term = spec["affinity"]["podAntiAffinity"]["requiredDuringSchedulingIgnoredDuringExecution"][0]
        self.assertEqual(term["topologyKey"], "kubernetes.io/hostname")
        self.assertEqual(term["labelSelector"]["matchLabels"], {"app": app})
        c = spec["containers"][0]
        self.assertEqual((c["image"], c["imagePullPolicy"]), (f"{app}:latest", "Never"))
        return d

    def test_deployments(self):
        self.check_deploy("product_catalog_deployment.yaml", "product-catalog", 2)
        self.check_deploy("shopping_cart_deployment.yaml", "shopping-cart", 3)

    def test_services_match_deployments(self):
        for svc_file, dep_file in (("product_catalog_service.yaml", "product_catalog_deployment.yaml"),
                                   ("shopping_cart_service.yaml", "shopping_cart_deployment.yaml")):
            svc, dep = self.load(svc_file), self.load(dep_file)
            self.assertEqual(svc["spec"]["type"], "NodePort")
            self.assertEqual(svc["metadata"]["namespace"], dep["metadata"]["namespace"])
            self.assertEqual(svc["spec"]["selector"], dep["spec"]["selector"]["matchLabels"])

    def test_replicas_fit_three_nodes(self):
        # required anti-affinity => replicas must be <= node count (3)
        for f in ("product_catalog_deployment.yaml", "shopping_cart_deployment.yaml"):
            self.assertLessEqual(self.load(f)["spec"]["replicas"], 3)


if __name__ == "__main__":
    unittest.main()
