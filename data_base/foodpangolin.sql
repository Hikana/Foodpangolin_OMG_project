-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-20 06:58:33
-- 伺服器版本： 10.4.32-MariaDB
-- PHP 版本： 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `foodpangolin`
--

-- --------------------------------------------------------

--
-- 資料表結構 `customer`
--

CREATE TABLE `customer` (
  `CustomerID` int(11) NOT NULL COMMENT '帥克ID',
  `name` varchar(255) NOT NULL COMMENT '帥克大名',
  `contactInfo` varchar(255) DEFAULT NULL COMMENT '聯繫資訊',
  `address` varchar(255) DEFAULT NULL COMMENT '地址阿寫可'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `deliveryperson`
--

CREATE TABLE `deliveryperson` (
  `id` int(11) NOT NULL COMMENT '小哥ID',
  `name` varchar(255) NOT NULL COMMENT '小哥大名',
  `vehicleInfo` varchar(255) DEFAULT NULL COMMENT '小bobo還是大bobo',
  `contactInfo` varchar(255) DEFAULT NULL COMMENT '小哥聯絡資訊'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `menu`
--

CREATE TABLE `menu` (
  `id` int(11) NOT NULL COMMENT '那道菜ID',
  `name` varchar(255) NOT NULL COMMENT '菜名',
  `price` float NOT NULL COMMENT '你要出多少',
  `description` text DEFAULT NULL COMMENT '好菜的介紹',
  `availabilityStatus` varchar(50) DEFAULT NULL COMMENT '賣完沒',
  `merchantId` int(11) NOT NULL COMMENT '商家ID'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `merchant`
--

CREATE TABLE `merchant` (
  `merchantid` int(11) NOT NULL COMMENT '商家流水號ID',
  `name` varchar(255) NOT NULL COMMENT '商家名稱',
  `location` varchar(255) DEFAULT NULL COMMENT '商家地點',
  `introduction` text DEFAULT NULL COMMENT '商家簡介',
  `contactInfo` varchar(255) DEFAULT NULL COMMENT '聯繫資訊'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `order`
--

CREATE TABLE `order` (
  `id` int(11) NOT NULL COMMENT '訂單流水號',
  `date` datetime NOT NULL COMMENT '啥時走的',
  `CustomerID` int(11) NOT NULL COMMENT '顧客ID',
  `merchantId` int(11) NOT NULL COMMENT '商家ID',
  `deliveryPersonId` int(11) DEFAULT NULL COMMENT '送貨員ID',
  `status` varchar(50) DEFAULT NULL COMMENT '狀態',
  `deliveryAddress` varchar(255) DEFAULT NULL COMMENT '地址',
  `totalPrice` float DEFAULT NULL COMMENT '總金額'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`CustomerID`);

--
-- 資料表索引 `deliveryperson`
--
ALTER TABLE `deliveryperson`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`id`),
  ADD KEY `merchantId` (`merchantId`);

--
-- 資料表索引 `merchant`
--
ALTER TABLE `merchant`
  ADD PRIMARY KEY (`merchantid`);

--
-- 資料表索引 `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customerId` (`CustomerID`),
  ADD KEY `merchantId` (`merchantId`),
  ADD KEY `deliveryPersonId` (`deliveryPersonId`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer`
--
ALTER TABLE `customer`
  MODIFY `CustomerID` int(11) NOT NULL AUTO_INCREMENT COMMENT '帥克ID';

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `deliveryperson`
--
ALTER TABLE `deliveryperson`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '小哥ID';

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `menu`
--
ALTER TABLE `menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '那道菜ID';

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `merchant`
--
ALTER TABLE `merchant`
  MODIFY `merchantid` int(11) NOT NULL AUTO_INCREMENT COMMENT '商家流水號ID';

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `order`
--
ALTER TABLE `order`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '訂單流水號';

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `menu`
--
ALTER TABLE `menu`
  ADD CONSTRAINT `menu_ibfk_1` FOREIGN KEY (`merchantId`) REFERENCES `merchant` (`merchantid`);

--
-- 資料表的限制式 `order`
--
ALTER TABLE `order`
  ADD CONSTRAINT `order_ibfk_1` FOREIGN KEY (`customerId`) REFERENCES `customer` (`CustomerID`),
  ADD CONSTRAINT `order_ibfk_2` FOREIGN KEY (`merchantId`) REFERENCES `merchant` (`merchantid`),
  ADD CONSTRAINT `order_ibfk_3` FOREIGN KEY (`deliveryPersonId`) REFERENCES `deliveryperson` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
