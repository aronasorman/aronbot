terraform {
  backend "gcs" {
    bucket  = "studio-aronbot-state"
    project = "contentworkshop-159920"
  }
}

resource "google_compute_address" "appserver-ip" {
  name    = "aronbot-appserver"
  project = "contentworkshop-159920"
  region  = "us-central1"
}

resource "google_compute_instance" "appserver" {
  name         = "aronbot-appserver"
  project      = "contentworkshop-159920"
  machine_type = "n1-standard-1"
  zone         = "us-central1-f"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-1804-lts"
    }
  }

  network_interface {
    network = "default"

    access_config {
      nat_ip = "${google_compute_address.appserver-ip.address}"
    }
  }
}

resource "google_sql_database_instance" "master-db" {
  name = "aronbot-master-db"
  database_version = "POSTGRES_9_6"
  region = "us-central1"
  project = "contentworkshop-159920"
  
  settings {
    tier = "db-f1-micro"
    
    backup_configuration {
      enabled = true
    }
  }
}
