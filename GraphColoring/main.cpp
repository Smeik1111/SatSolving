#include <iostream>
#include "../ipasir-master/ipasir.h"
#include "../picosat-965/picosat.h"

int main()
{
    std::cout << "Hello World" << std::endl;
    auto picosat = picosat_init();
    picosat_add(picosat, -3);
    picosat_add(picosat, 2);
    picosat_add(picosat, 0);
    picosat_add(picosat, -3);
    picosat_add(picosat, -2);
    picosat_add(picosat, 1);
    picosat_add(picosat, 0);
    picosat_add(picosat, 3);
    picosat_add(picosat, 0);

    picosat_sat(picosat, -1);

    //auto ipasir = ipasir_init();

}