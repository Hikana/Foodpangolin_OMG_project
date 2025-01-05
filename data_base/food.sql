-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2025-01-05 16:43:45
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
-- 資料庫： `food`
--

-- --------------------------------------------------------

--
-- 資料表結構 `customer`
--

CREATE TABLE `customer` (
  `id` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `name` varchar(10) NOT NULL,
  `contact` varchar(10) NOT NULL,
  `address` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `customer`
--

INSERT INTO `customer` (`id`, `uid`, `name`, `contact`, `address`) VALUES
(1, 1, '孫睿君', '0912345678', 'dsryhftduhsrujsxzr');

-- --------------------------------------------------------

--
-- 資料表結構 `customer_comment`
--

CREATE TABLE `customer_comment` (
  `comment_id` int(10) NOT NULL,
  `customer_order_id` int(10) NOT NULL,
  `comment` text NOT NULL,
  `rating` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `customer_comment`
--

INSERT INTO `customer_comment` (`comment_id`, `customer_order_id`, `comment`, `rating`) VALUES
(1, 0, '4', 123),
(2, 0, '5', 123),
(3, 0, '5', 125);

-- --------------------------------------------------------

--
-- 資料表結構 `customer_order`
--

CREATE TABLE `customer_order` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `store_id` int(11) NOT NULL,
  `delivery_id` int(11) NOT NULL,
  `destination` text NOT NULL,
  `quantity` int(10) NOT NULL,
  `status` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `customer_order`
--

INSERT INTO `customer_order` (`id`, `customer_id`, `store_id`, `delivery_id`, `destination`, `quantity`, `status`, `time`) VALUES
(1, 1, 1, 1, '暨大', 5, 4, '2025-01-05 13:07:26'),
(2, 1, 1, 1, '暨大', 4, 4, '2025-01-05 13:11:51'),
(3, 1, 1, -1, '全家', 1, 0, '2025-01-05 13:11:45');

-- --------------------------------------------------------

--
-- 資料表結構 `customer_order_history`
--

CREATE TABLE `customer_order_history` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `delivery`
--

CREATE TABLE `delivery` (
  `id` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `name` varchar(10) NOT NULL,
  `license_plate` varchar(8) NOT NULL,
  `contact` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `delivery`
--

INSERT INTO `delivery` (`id`, `uid`, `name`, `license_plate`, `contact`) VALUES
(1, 2, '送貨員', 'ABC-123', '09123456789');

-- --------------------------------------------------------

--
-- 資料表結構 `order_menu`
--

CREATE TABLE `order_menu` (
  `id` int(11) NOT NULL,
  `menu_id` int(11) NOT NULL,
  `customer_order_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `order_menu`
--

INSERT INTO `order_menu` (`id`, `menu_id`, `customer_order_id`) VALUES
(7, 9, 8),
(8, 9, 9),
(9, 9, 10),
(10, 9, 11),
(11, 9, 12),
(12, 9, 13),
(13, 9, 14),
(14, 9, 15),
(15, 9, 16),
(16, 9, 17),
(17, 9, 1),
(18, 9, 2),
(19, 9, 3);

-- --------------------------------------------------------

--
-- 資料表結構 `role`
--

CREATE TABLE `role` (
  `id` int(11) NOT NULL,
  `name` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `role`
--

INSERT INTO `role` (`id`, `name`) VALUES
(1, '店家'),
(2, '顧客'),
(3, '外送員');

-- --------------------------------------------------------

--
-- 資料表結構 `status`
--

CREATE TABLE `status` (
  `id` int(10) NOT NULL,
  `status` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `status`
--

INSERT INTO `status` (`id`, `status`) VALUES
(0, '餐點製作中'),
(1, '待運送'),
(2, '運送中'),
(3, '已送達'),
(4, '已簽收');

-- --------------------------------------------------------

--
-- 資料表結構 `store`
--

CREATE TABLE `store` (
  `id` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `location` text NOT NULL,
  `intro` text NOT NULL,
  `contact` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `store`
--

INSERT INTO `store` (`id`, `uid`, `name`, `location`, `intro`, `contact`) VALUES
(1, 3, '全家', '南投縣埔里鎮大學路 XX 號', '24 小時', '09123456789'),
(2, 4, '小七', '埔里鎮中山街2段', '有7-11真好', '049-5544887');

-- --------------------------------------------------------

--
-- 資料表結構 `store_menu`
--

CREATE TABLE `store_menu` (
  `id` int(11) NOT NULL,
  `sid` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `price` int(11) NOT NULL,
  `intro` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `store_menu`
--

INSERT INTO `store_menu` (`id`, `sid`, `name`, `price`, `intro`) VALUES
(9, 1, '炒飯111', 75, '好吃好吃'),
(10, 1, '雪碧', 25, '配花椒很好喝');

-- --------------------------------------------------------

--
-- 資料表結構 `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `role` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `role`) VALUES
(1, 'srj_cus', '123456', 2),
(2, 'ccc_dlv', '123456', 3),
(3, 'aa_str', '123456', 1),
(4, 'plt', '123456', 4);

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `customer_comment`
--
ALTER TABLE `customer_comment`
  ADD PRIMARY KEY (`comment_id`);

--
-- 資料表索引 `customer_order`
--
ALTER TABLE `customer_order`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `customer_order_history`
--
ALTER TABLE `customer_order_history`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `delivery`
--
ALTER TABLE `delivery`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `order_menu`
--
ALTER TABLE `order_menu`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `store`
--
ALTER TABLE `store`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `store_menu`
--
ALTER TABLE `store_menu`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer`
--
ALTER TABLE `customer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer_comment`
--
ALTER TABLE `customer_comment`
  MODIFY `comment_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer_order`
--
ALTER TABLE `customer_order`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer_order_history`
--
ALTER TABLE `customer_order_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `delivery`
--
ALTER TABLE `delivery`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `order_menu`
--
ALTER TABLE `order_menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `role`
--
ALTER TABLE `role`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `store`
--
ALTER TABLE `store`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `store_menu`
--
ALTER TABLE `store_menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
