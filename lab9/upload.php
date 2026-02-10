<?php
// upload.php
// Lab 9: SROS2 keystore receiver (training only)

date_default_timezone_set('UTC');

$upload_dir = __DIR__ . "/keystores/";
if (!file_exists($upload_dir)) {
    mkdir($upload_dir, 0755, true);
}

if (!isset($_FILES['file'])) {
    http_response_code(400);
    echo "No file uploaded\n";
    exit;
}

$file = $_FILES['file'];

if ($file['error'] !== UPLOAD_ERR_OK) {
    http_response_code(500);
    echo "Upload error\n";
    exit;
}

// 生成唯一文件名（避免覆盖）
$timestamp = date("Ymd_His");
$client_ip = $_SERVER['REMOTE_ADDR'];
$safe_ip = str_replace(":", "_", $client_ip);

$filename = "keystore_{$safe_ip}_{$timestamp}.tar.gz";
$dest = $upload_dir . $filename;

if (move_uploaded_file($file['tmp_name'], $dest)) {
    echo "OK\n";
    echo "Saved as: {$filename}\n";
} else {
    http_response_code(500);
    echo "Failed to save file\n";
}
?>
