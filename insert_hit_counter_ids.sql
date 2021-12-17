CREATE TABLE `hippocampome`.`counters_db_id` (
  `database_id` int NOT NULL,
  PRIMARY KEY (`database_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `hippocampome`.counters_db_id (`database_id`) VALUES ('1');

CREATE TABLE `hippodevome`.`counters_db_id` (
  `database_id` int NOT NULL,
  PRIMARY KEY (`database_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `hippodevome`.counters_db_id (`database_id`) VALUES ('2');

CREATE TABLE `hipporevome`.`counters_db_id` (
  `database_id` int NOT NULL,
  PRIMARY KEY (`database_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `hipporevome`.counters_db_id (`database_id`) VALUES ('3');

CREATE TABLE `hippodevur2`.`counters_db_id` (
  `database_id` int NOT NULL,
  PRIMARY KEY (`database_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `hippodevur2`.counters_db_id (`database_id`) VALUES ('4');