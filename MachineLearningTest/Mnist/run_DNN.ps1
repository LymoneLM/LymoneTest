# 定义参数范围
$batch_sizes = @(32, 64, 128, 256)
$learning_rates = @(0.1, 0.05, 0.01, 0.005, 0.001)
$epochs_list = @(10, 15, 20, 25)

# 创建20组实验配置
$experiments = @()
for ($i = 0; $i -lt 20; $i++) {
    $params = @{
        batch_size = $batch_sizes | Get-Random
        learning_rate = $learning_rates | Get-Random
        epochs = $epochs_list | Get-Random
        exp_no = $i
    }
    $experiments += $params
}

# 确保输出目录存在
$outputDir = "./output"
if (-not (Test-Path -Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# 运行所有实验
foreach ($exp in $experiments) {
    Write-Host ("`n" + ('=' * 60))
    Write-Host "Starting experiment $($exp.exp_no) with params:"
    Write-Host "  Batch size: $($exp.batch_size)"
    Write-Host "  Learning rate: $($exp.learning_rate)"
    Write-Host "  Epochs: $($exp.epochs)"
    Write-Host ('=' * 60)

    # 构建Python命令
    $outputFile = "$outputDir/DNN_output_$($exp.exp_no).txt"
    $arguments = @(
        "1_Mnist_DNN.py",
        "-b", $exp.batch_size,
        "-l", $exp.learning_rate,
        "-e", $exp.epochs,
        "-n", $exp.exp_no
    )

    # 执行命令并重定向输出
    python $arguments *> $outputFile
}

Write-Host "`nAll experiments completed!"