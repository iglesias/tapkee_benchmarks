echo ====LLE====
echo "Swissroll 5000"
./tapkee/tapkee -i data/swissroll5000.dat -o /dev/null -m klle -k 20 --benchmark
echo "Swissroll 10000"
./tapkee/tapkee -i data/swissroll10000.dat -o /dev/null -m klle -k 20 --benchmark
echo "MNIST 2000"
./tapkee/tapkee -i data/mnist2000.dat -o /dev/null -m klle -k 20 --benchmark
echo "MNIST 4000"
./tapkee/tapkee -i data/mnist4000.dat -o /dev/null -m klle -k 20 --benchmark
echo "MIT-CBCL"
./tapkee/tapkee -i data/cbcl.dat -o /dev/null -m klle -k 20 --benchmark
