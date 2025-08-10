# Phoenix Recovery

Phoenix Recovery is a comprehensive FAT32 data recovery tool designed for recovering lost files from storage devices like USB drives, hard drives, and memory cards. The tool uses advanced techniques including orphan cluster analysis, machine learning-based similarity detection, and direct filesystem manipulation to reconstruct deleted files and restore file system integrity.

## 🚀 Features

- **FAT32 Filesystem Recovery**: Specialized recovery for FAT32 formatted storage devices
- **Orphan Cluster Detection**: Identifies and analyzes orphaned clusters containing file data
- **Machine Learning Integration**: Uses sentence transformers and K-means clustering for intelligent file reconstruction
- **Interactive GUI**: Modern Tkinter-based user interface for easy file recovery
- **Direct Filesystem Access**: Low-level access to modify FAT tables and directory entries
- **Multi-Platform Support**: Works on Windows, Linux, and macOS
- **Real-time Recovery**: Immediate file recovery with progress tracking

## 🏗️ Architecture

The project consists of several core modules:

### Core Recovery Engine
- **`main_recovery.py`**: Main recovery orchestration logic
- **`orphanClusters.py`**: Orphan cluster detection and analysis
- **`total_clusters.py`**: Filesystem cluster calculations
- **`file_span.py`**: File cluster span calculations

### Filesystem Manipulation
- **`edit_fat_table.py`**: FAT table modification utilities
- **`edit_dir_table.py`**: Directory table manipulation
- **`list_deleted_files.py`**: Deleted file detection and listing

### Machine Learning Components
- **`model.py`**: ML-based cluster similarity analysis using sentence transformers
- **`updateCSV.py`**: Data preprocessing and CSV management for ML training

### System Integration
- **`get_drive.py`**: System disk detection and enumeration
- **`get_Clusters.py`**: Cluster content extraction and analysis

### User Interface
- **`index.py`**: Main Tkinter GUI application

## 📋 Prerequisites

### System Requirements
- Python 3.7 or higher
- Administrative/root privileges (required for direct disk access)
- Minimum 4GB RAM (for ML operations)
- FAT32 formatted storage device

### Python Dependencies
```bash
pip install pandas
pip install sentence-transformers
pip install scikit-learn
pip install numpy
pip install psutil
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd phoenix
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python index.py
   ```

## 🚀 Usage

### Quick Start
1. **Run the application with administrative privileges**
   ```bash
   # Windows (PowerShell as Administrator)
   python index.py
   
   # Linux/macOS
   sudo python3 index.py
   ```

2. **Select your target disk** from the dropdown menu
3. **Click "Load Disk Data"** to scan for deleted files
4. **Select a file** from the recovery list
5. **Click "Select File"** to initiate recovery

### Command Line Usage

#### List Connected Disks
```python
from get_drive import list_connected_disks
disks = list_connected_disks()
print(f"Available disks: {disks}")
```

#### Scan for Deleted Files
```python
from list_deleted_files import list_deleted_files
deleted_files = list_deleted_files("/dev/sda1")  # Replace with your disk path
```

#### Manual Recovery
```python
from main_recovery import recovery_func
success = recovery_func("document.txt", 1234, 1024, "/dev/sda1")
```

#### ML-Based Cluster Analysis
```python
from model import recover
grouped_clusters = recover("data.csv", [1,2,3,4,5], n_clusters=3, start_cluster=1)
```

## 🔧 Configuration

### Data File
The `data.csv` file contains training data for the machine learning model:
- `cluster_number`: Cluster identifier
- `content`: Text content extracted from clusters

### ML Model Settings
- **Model**: `all-MiniLM-L6-v2` (sentence transformer)
- **Clustering**: K-means with cosine similarity
- **Default clusters**: 5 groups

## 📁 Project Structure

```
phoenix/
├── index.py                 # Main GUI application
├── main_recovery.py         # Recovery orchestration
├── orphanClusters.py        # Orphan cluster detection
├── model.py                 # ML-based similarity analysis
├── edit_fat_table.py        # FAT table manipulation
├── edit_dir_table.py        # Directory table operations
├── list_deleted_files.py    # Deleted file detection
├── total_clusters.py        # Cluster calculations
├── file_span.py            # File span analysis
├── get_drive.py            # Disk detection
├── get_Clusters.py         # Cluster content extraction
├── updateCSV.py            # Data preprocessing
├── data.csv                # ML training data
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## ⚠️ Important Notes

### Security Considerations
- **Always run with administrative privileges** for disk access
- **Backup important data** before attempting recovery
- **Verify disk paths** to avoid data loss on wrong devices
- **Unmount drives** before recovery operations

### Limitations
- **FAT32 only**: Does not support NTFS, exFAT, or other filesystems
- **File size**: Limited by FAT32's 4GB file size restriction
- **Cluster size**: Recovery depends on filesystem cluster configuration
- **Data integrity**: Success depends on cluster fragmentation and corruption level

### Performance
- **Large drives**: Scanning may take time on high-capacity devices
- **ML operations**: First run may download model weights (~90MB)
- **Memory usage**: Increases with cluster count and content size

## 🐛 Troubleshooting

### Common Issues

#### Permission Denied
```bash
# Windows: Run PowerShell as Administrator
# Linux/macOS: Use sudo
sudo python3 index.py
```

#### Disk Not Found
- Verify disk path exists
- Ensure disk is not mounted
- Check device permissions

#### Recovery Failure
- Verify filesystem is FAT32
- Check cluster integrity
- Ensure sufficient free space

#### ML Model Errors
```bash
# Clear model cache
rm -rf ~/.cache/torch/sentence_transformers/
# Reinstall dependencies
pip install --force-reinstall sentence-transformers
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests if applicable**
5. **Submit a pull request**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FAT32 Specification**: Microsoft Corporation
- **Sentence Transformers**: Hugging Face
- **Scikit-learn**: INRIA, Telecom ParisTech
- **Tkinter**: Python Software Foundation

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/phoenix/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/phoenix/discussions)
- **Documentation**: [Wiki](https://github.com/your-repo/phoenix/wiki)

## 🔄 Version History

- **v1.0.0**: Initial release with basic recovery functionality
- **v1.1.0**: Added machine learning capabilities
- **v1.2.0**: Enhanced GUI and error handling
- **v1.3.0**: Improved cluster analysis and recovery success rate

---

**⚠️ Disclaimer**: This tool performs low-level filesystem operations. Always backup your data before use. The developers are not responsible for any data loss or corruption.
