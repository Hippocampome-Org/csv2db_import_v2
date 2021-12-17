CREATE TABLE `SynproParcelVolumes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subregion` varchar(500) DEFAULT NULL,
  `parcel` varchar(500) DEFAULT NULL,
  `volume` decimal(20,6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
