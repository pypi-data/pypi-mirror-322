aimsChain
=========
aimsChain developed for FHI-aims ( https://fhi-aims.org/ )

**A package for finding minimum energy path and transition state:** This project aims to provide an all-in-one package for various flavours of the chain of states methods for finding the minimum energy path(MEP). Currently the nudged elastic band method (NEB)[1, 2], the string method[3], and the growing string method[4] are included.

For usage please refer to FHI-aims manual.

originally developed by Yingyu Yao ( https://github.com/yingyuyao/aimsChain ) -  yaoyingyu(at)hotmail.com

The aimsChain code is distributed under the Lesser General Public License as published in Version 3, 29 June 2007, at http://www.gnu.org/licenses/lgpl.html . Some of the optimizer routines in the code originated within the Atomic Simulation Environment
(ASE) https://wiki.fysik.dtu.dk/ase [5]. We wish to give full credit to the developers of these routines and original authors - Yingyu Yao and people involved in ASE [5].

Python2 to Python3 transition and update of the test done by Ondrej Krejci, CEST group, Aalto University 2022 - ondrej.krejci(at)aalto.fi. I cannot develop and maintain the code in the future. If you are interested, please contact me and FHI-aims team (Ideally via a Slack channel) to take over it. 

Tests are in the samples directory together with their optimized results; except for sample5 examples, which never run!
sample7 and sample7.1 are almost the same; just there are 10 inner images in 7.1 (instead of 3) and the first image is slightly shifted.

Literature
==========
[1] G. Mills K. W. Jacobsen H. Jonsson. Nudged Elastic Band Method for Finding Minimum Energy Paths of Transitions. World Scientific, 1998.

[2] G. Henkelman, B. P. Uberuagga, and H. Jonsson. A climbing image nudged elastic band method for finding saddle points and minimum energy paths. J. Chem. Phys., 113:9901, 2000.

[3] E Weinan, Weiqing Ren, and Eric Vanden-Eijnden. Simplified and improved string method for computing the minimum energy paths in barrier-crossing events. J. Chem. Phys., 126:164103, 2007. 

[4] Baron Peters, Andreas Heyden, Alexis T. Bell, and Arup Chakraborty. A growing string method for determining transition states: Comparison to the nudged elastic band and string methods. The Journal of Chemical Physics, 120(17):7877–7886, 2004. 

[5] Ask Hjorth Larsen, Jens Jørgen Mortensen, Jakob Blomqvist, Ivano E. Castelli, Rune Christensen, Marcin Dułak, Jesper Friis, Michael N. Groves, Bjørk Hammer, Cory Hargus, Eric D. Hermes, Paul C. Jennings, Peter Bjerre Jensen, James Kermode, John R. Kitchin, Esben Leonhard Kolsbjerg, Joseph Kubal, Kristen Kaasbjerg, Steen Lysgaard, Jón Bergmann Maronsson, Tristan Maxson, Thomas Olsen, Lars Pastewka, Andrew Peterson, Carsten Rostgaard, Jakob Schiøtz, Ole Schütt, Mikkel Strange, Kristian S. Thygesen, Tejs Vegge, Lasse Vilhelmsen, Michael Walter, Zhenhua Zeng, Karsten Wedel Jacobsen. The Atomic Simulation Environment—A Python library for working with atoms. J. Phys.: Condens. Matter Vol. 29 273002, 2017
