def message():
    print("Hello, World!")

if __name__ == "__main__":
    message()

CREATE TABLE arrival (
  id_arrival int (10) AUTO_INCREMENT,
  id_track int (10) NOT NULL,
  id_competition int (10) NOT NULL,
  id_crew int (10) NOT NULL,
  result text,
  PRIMARY KEY (id_arrival),
  FOREIGN KEY (id_track) REFERENCES track (id_track),
  FOREIGN KEY (id_competition) REFERENCES competition (id_competition),
);

CREATE TABLE crew_arrival (
  crew_arrival int (10) AUTO_INCREMENT,
  id_crew int (10) NOT NULL,
  id_arrival int (10) NOT NULL,
  FOREIGN KEY (id_crew) REFERENCES crew (id_crew),
  FOREIGN KEY (id_arrival) REFERENCES arrival (id_arrival),
  PRIMARY KEY (crew_arrival)
);

CREATE TABLE crew (
  id_crew int (10) AUTO_INCREMENT,
  id_racer int (10) NOT NULL,
  id_navigator int (10) NOT NULL,
  id_car int (10) NOT NULL,
  status text,
  PRIMARY KEY (id_crew),
  FOREIGN KEY (id_racer) REFERENCES racer (id_racer),
  FOREIGN KEY (id_navigator) REFERENCES navigator (id_navigator),
  FOREIGN KEY (id_car) REFERENCES car (id_car)
  );
