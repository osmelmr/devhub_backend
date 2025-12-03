-- Limpiar tablas primero (opcional - solo si quieres empezar desde cero)
DELETE FROM products_product;
DELETE FROM categories_category;

-- Insertar datos de prueba para Categories
INSERT INTO categories_category (id, owner_id, name) VALUES
-- Categorías para usuario 1
('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'user1234567890abcdef1234567890abcd', 'Electrónicos Usuario1'),
('b2c3d4e5-f6g7-8901-bcde-f234567890ab', 'user1234567890abcdef1234567890abcd', 'Ropa y Moda'),
('c3d4e5f6-g7h8-9012-cdef-34567890abcd', 'user1234567890abcdef1234567890abcd', 'Hogar y Jardín'),

-- Categorías para usuario 2
('d4e5f6g7-h8i9-0123-defg-4567890abcde', 'userabcdef1234567890abcdef12345678', 'Libros y Literatura'),
('e5f6g7h8-i9j0-1234-efgh-567890abcdef', 'userabcdef1234567890abcdef12345678', 'Deportes y Aire Libre');

-- Insertar datos de prueba para Products
INSERT INTO products_product (
    id, owner_id, name, slug, description, category_id, category_name, 
    price, discount, stock, rating, status, image, image_public_id, 
    created_at, updated_at
) VALUES
-- Productos para usuario 1 en categoría Electrónicos
(
    'f6g7h8i9-j0k1-2345-fghi-67890abcdef1',
    'user1234567890abcdef1234567890abcd',
    'iPhone 14 Pro',
    'iphone-14-pro',
    'El último smartphone de Apple con cámara de 48MP y Dynamic Island',
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    'Electrónicos Usuario1',
    999.99,
    10.00,
    25,
    4.5,
    'active',
    'https://example.com/images/iphone14pro.jpg',
    'products/iphone14pro_abc123',
    '2024-01-15 10:30:00',
    '2024-01-15 10:30:00'
),
(
    'g7h8i9j0-k1l2-3456-hijk-7890abcdef12',
    'user1234567890abcdef1234567890abcd',
    'MacBook Air M2',
    'macbook-air-m2',
    'Laptop ultradelgada con chip M2 de Apple, perfecta para trabajo y creatividad',
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    'Electrónicos Usuario1',
    1199.99,
    0.00,
    15,
    4.8,
    'active',
    'https://example.com/images/macbookairm2.jpg',
    'products/macbookairm2_def456',
    '2024-01-16 14:20:00',
    '2024-01-20 09:15:00'
),

-- Productos para usuario 1 en categoría Ropa
(
    'h8i9j0k1-l2m3-4567-ijkl-890abcdef123',
    'user1234567890abcdef1234567890abcd',
    'Camiseta Básica Algodón',
    'camiseta-basica-algodon',
    'Camiseta 100% algodón de alta calidad, disponible en múltiples colores',
    'b2c3d4e5-f6g7-8901-bcde-f234567890ab',
    'Ropa y Moda',
    19.99,
    15.00,
    100,
    4.2,
    'active',
    'https://example.com/images/camiseta-algodon.jpg',
    'products/camiseta_ghi789',
    '2024-01-17 11:45:00',
    '2024-01-17 11:45:00'
),
(
    'i9j0k1l2-m3n4-5678-jklm-90abcdef1234',
    'user1234567890abcdef1234567890abcd',
    'Jeans Slim Fit',
    'jeans-slim-fit',
    'Jeans de corte slim fit, color azul oscuro, talle europeo',
    'b2c3d4e5-f6g7-8901-bcde-f234567890ab',
    'Ropa y Moda',
    49.99,
    20.00,
    0,
    4.0,
    'out_of_stock',
    'https://example.com/images/jeans-slim.jpg',
    'products/jeans_jkl012',
    '2024-01-18 16:30:00',
    '2024-01-25 08:45:00'
),

-- Productos para usuario 1 en categoría Hogar
(
    'j0k1l2m3-n4o5-6789-klmn-0abcdef12345',
    'user1234567890abcdef1234567890abcd',
    'Juego de Sábanas Queen',
    'juego-de-sabanas-queen',
    'Juego de sábanas de algodón egipcio, tamaño queen, varios colores disponibles',
    'c3d4e5f6-g7h8-9012-cdef-34567890abcd',
    'Hogar y Jardín',
    79.99,
    25.00,
    30,
    4.6,
    'active',
    'https://example.com/images/sabanas-queen.jpg',
    'products/sabanas_mno345',
    '2024-01-19 13:15:00',
    '2024-01-19 13:15:00'
),

-- Productos para usuario 2 en categoría Libros
(
    'k1l2m3n4-o5p6-7890-lmno-abcdef123456',
    'userabcdef1234567890abcdef12345678',
    'Cien Años de Soledad',
    'cien-anos-de-soledad',
    'Novela clásica de Gabriel García Márquez, edición especial',
    'd4e5f6g7-h8i9-0123-defg-4567890abcde',
    'Libros y Literatura',
    24.99,
    0.00,
    50,
    4.9,
    'active',
    'https://example.com/images/cien-anos-soledad.jpg',
    'products/libro_pqr678',
    '2024-01-20 09:00:00',
    '2024-01-20 09:00:00'
),
(
    'l2m3n4o5-p6q7-8901-mnop-bcdef1234567',
    'userabcdef1234567890abcdef12345678',
    'El Principito',
    'el-principito',
    'Edición ilustrada del clásico de Antoine de Saint-Exupéry',
    'd4e5f6g7-h8i9-0123-defg-4567890abcde',
    'Libros y Literatura',
    18.99,
    10.00,
    75,
    4.7,
    'active',
    'https://example.com/images/principito.jpg',
    'products/libro_stu901',
    '2024-01-21 15:45:00',
    '2024-01-22 10:30:00'
),

-- Productos para usuario 2 en categoría Deportes
(
    'm3n4o5p6-q7r8-9012-nopq-cdef12345678',
    'userabcdef1234567890abcdef12345678',
    'Pelota de Fútbol Profesional',
    'pelota-de-futbol-profesional',
    'Pelota oficial tamaño 5, ideal para partidos profesionales',
    'e5f6g7h8-i9j0-1234-efgh-567890abcdef',
    'Deportes y Aire Libre',
    89.99,
    15.00,
    20,
    4.4,
    'active',
    'https://example.com/images/pelota-futbol.jpg',
    'products/pelota_vwx234',
    '2024-01-22 12:00:00',
    '2024-01-22 12:00:00'
),
(
    'n4o5p6q7-r8s9-0123-opqr-def123456789',
    'userabcdef1234567890abcdef12345678',
    'Raqueta de Tenis',
    'raqueta-de-tenis',
    'Raqueta profesional de tenis, peso balanceado, grip ergonómico',
    'e5f6g7h8-i9j0-1234-efgh-567890abcdef',
    'Deportes y Aire Libre',
    129.99,
    30.00,
    0,
    4.3,
    'inactive',
    'https://example.com/images/raqueta-tenis.jpg',
    'products/raqueta_yza567',
    '2024-01-23 14:20:00',
    '2024-01-28 11:10:00'
),

-- Producto adicional para mostrar diferentes estados
(
    'o5p6q7r8-s9t0-1234-pqrs-ef1234567890',
    'user1234567890abcdef1234567890abcd',
    'Auriculares Inalámbricos',
    'auriculares-inalambricos',
    'Auriculares Bluetooth con cancelación de ruido y 30h de batería',
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    'Electrónicos Usuario1',
    199.99,
    0.00,
    0,
    4.1,
    'out_of_stock',
    'https://example.com/images/auriculares.jpg',
    'products/auriculares_bcd890',
    '2024-01-24 17:30:00',
    '2024-01-29 16:45:00'
);