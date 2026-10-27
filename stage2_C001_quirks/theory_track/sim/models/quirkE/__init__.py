import particles
import couplings
import lorentz
import parameters
import vertices
import coupling_orders
import function_library
import object_library
#from . import write_param_card
try:
    import decays
except ImportError:
    pass    
try:
    from . import build_restrict
except ImportError:
    pass

# model options
gauge = [0, 1]


all_particles = particles.all_particles
all_vertices = vertices.all_vertices
all_couplings = couplings.all_couplings
all_lorentz = lorentz.all_lorentz
all_parameters = parameters.all_parameters
all_orders = coupling_orders.all_orders
all_functions = function_library.all_functions
#all_decays = decays.all_decays


__author__ = "SM: N. Christensen, C. Duhr (MG5 sm v1.3); quirk E/Etilde additions hand-written (E4, 2026-10-11)"
__version__ = "1.3"
__email__ = "neil@pa.msu.edu, claude.duhr@uclouvain.be"
