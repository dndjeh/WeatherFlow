-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema toy_project
-- -----------------------------------------------------
-- CREATE SCHEMA IF NOT EXISTS `toy_project` DEFAULT CHARACTER SET utf8 

-- -----------------------------------------------------
-- Schema toy_project
--
-- CREATE SCHEMA IF NOT EXISTS `toy_project` DEFAULT CHARACTER SET utf8 
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `toy_project` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;
USE `toy_project` ;

-- -----------------------------------------------------
-- Table `toy_project`.`ROAD_ID`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `toy_project`.`ROAD_ID` (
  `LINK_ID` VARCHAR(45) NOT NULL,
  `GRS80TM_X` FLOAT NOT NULL,
  `GRS80TM_Y` FLOAT NOT NULL,
  `VER_SEQ` VARCHAR(3) NOT NULL,
  PRIMARY KEY (`LINK_ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `toy_project`.`OUTBREAK_CODE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `toy_project`.`OUTBREAK_CODE` (
  `ACC_TYPE` VARCHAR(5) NOT NULL,
  `ACC_TYPE_NM` VARCHAR(15) NULL,
  PRIMARY KEY (`ACC_TYPE`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `toy_project`.`OUTBREAK_DETAIL_CODE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `toy_project`.`OUTBREAK_DETAIL_CODE` (
  `ACC_DTYPE` VARCHAR(10) NOT NULL,
  `ACC_DTYPE_NM` VARCHAR(15) NULL,
  PRIMARY KEY (`ACC_DTYPE`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `toy_project`.`OUTBREAK`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `toy_project`.`OUTBREAK` (
  `ACC_ID` VARCHAR(5) NOT NULL,
  `LINK_ID` VARCHAR(45) NOT NULL,
  `OCCR_DATE` DATE NOT NULL,
  `OCCR_TIME` TIME NOT NULL,
  `EXP_CLR_DATE` DATE NOT NULL,
  `EXP_CLR_TIME` TIME NOT NULL,
  `ACC_TYPE` VARCHAR(45) NOT NULL,
  `ACC_DTYPE` VARCHAR(10) NOT NULL,
  `ACC_INFO` TINYTEXT NOT NULL,
  `OUTBREAK_DETAIL_CODE_ACC_DTYPE` VARCHAR(10) NOT NULL,
  `OUTBREAK_CODE_ACC_TYPE` VARCHAR(5) NOT NULL,
  PRIMARY KEY (`ACC_ID`),
  INDEX `LINK_ID_idx` (`LINK_ID` ASC) VISIBLE,
  INDEX `ACC_TYPE_idx` (`ACC_TYPE` ASC) VISIBLE,
  INDEX `ACC_TYPE_NM_idx` (`ACC_DTYPE` ASC) VISIBLE,
  CONSTRAINT `fk_OUTBREAK_ROAD_ID_LINK_ID`
    FOREIGN KEY (`LINK_ID`)
    REFERENCES `toy_project`.`ROAD_ID` (`LINK_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_OUTBREAK_OUTBREAK_CODE_ACC_TYPE`
    FOREIGN KEY (`ACC_TYPE`)
    REFERENCES `toy_project`.`OUTBREAK_CODE` (`ACC_TYPE`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_OUTBREAK_OUTBREAK_DETAIL_CODE_ACC_TYPE_NM`
    FOREIGN KEY (`ACC_DTYPE`)
    REFERENCES `toy_project`.`OUTBREAK_DETAIL_CODE` (`ACC_DTYPE`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `toy_project`.`REGION`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `toy_project`.`REGION` (
  `GU_CODE` INT NOT NULL,
  `GU_NAME` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`GU_CODE`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `toy_project`.`RAIN`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `toy_project`.`RAIN` (
  `GU_CODE` INT NOT NULL,
  `RAINFALL10` INT NULL,
  `RECEIVE_TIME` VARCHAR(45) NULL,
  PRIMARY KEY (`GU_CODE`),
  CONSTRAINT `fk_RAIN_REGION_GU_CODE`
    FOREIGN KEY (`GU_CODE`)
    REFERENCES `toy_project`.`REGION` (`GU_CODE`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `toy_project`.`ROAD_TRAFFIC`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `toy_project`.`ROAD_TRAFFIC` (
  `LINK_ID` VARCHAR(45) NOT NULL,
  `PRCS_SPD` VARCHAR(45) NULL,
  `PRCS_TRV_TIME` INT NULL,
  PRIMARY KEY (`LINK_ID`),
  CONSTRAINT `fk_ROAD_TRAFFIC_ROAD_IDLINK_ID`
    FOREIGN KEY (`LINK_ID`)
    REFERENCES `toy_project`.`ROAD_ID` (`LINK_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
