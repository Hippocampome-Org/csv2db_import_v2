CREATE TABLE `SynproNOCR` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source_ID` varchar(400) DEFAULT NULL,
  `source_Name` varchar(400) DEFAULT NULL,
  `source_E_or_I` varchar(400) DEFAULT NULL,
  `target_ID` varchar(400) DEFAULT NULL,
  `target_Name` varchar(400) DEFAULT NULL,
  `target_E_or_I` varchar(400) DEFAULT NULL,
  `type` varchar(400) DEFAULT NULL,
  `layers` varchar(400) DEFAULT NULL,
  `neurite` varchar(400) DEFAULT NULL,
  `neurite_id` varchar(400) DEFAULT NULL,
  `potential_synapses` varchar(400) DEFAULT NULL,
  `number_of_contacts` varchar(400) DEFAULT NULL,
  `probability` varchar(400) DEFAULT NULL,
  `connection` varchar(400) DEFAULT NULL,
  `ES` varchar(400) DEFAULT NULL,
  `ES_PMID` varchar(400) DEFAULT NULL,
  `refIDs` varchar(400) DEFAULT NULL,
  `notes` varchar(400) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6357 DEFAULT CHARSET=utf8;
