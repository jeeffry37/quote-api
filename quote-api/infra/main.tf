resource "kubernetes_namespace" "quote" {
  metadata {
    name = "quote-api"
  }
}

resource "kubernetes_deployment" "api" {
  metadata {
    name      = "quote-api"
    namespace = kubernetes_namespace.quote.metadata[0].name
    labels = {
      app = "quote-api"
    }
  }

  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "quote-api"
      }
    }
    template {
      metadata {
        labels = {
          app = "quote-api"
        }
      }
      spec {
        container {
          name  = "quote-api"
          image = "jeeffry/quote-api:1.0"
          port {
            container_port = 5000
          }
          env {
            name  = "QUOTES_PATH"
            value = "/app/quotes.json"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "api" {
  metadata {
    name      = "quote-api-service"
    namespace = kubernetes_namespace.quote.metadata[0].name
  }

  spec {
    selector = {
      app = "quote-api"
    }
    port {
      port        = 80
      target_port = 5000
    }
    type = "NodePort"
  }
}

