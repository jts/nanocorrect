# Copyright (c) 2011-2013, Pacific Biosciences of California, Inc.
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted (subject to the limitations in the
# disclaimer below) provided that the following conditions are met:
# 
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
# 
#  * Neither the name of Pacific Biosciences nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
# 
# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE
# GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED BY PACIFIC
# BIOSCIENCES AND ITS CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL PACIFIC BIOSCIENCES OR ITS
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
# 
unitigger = bogart
#utgErrorRate = 0.015 
#utgErrorLimit = 4.5

cnsErrorRate = 0.25
cgwErrorRate = 0.25

#ovlErrorRate = 0.015
ovlErrorRate = 0.08

frgMinLen = 1000
ovlMinLen = 40
  
merSize=14

merylMemory = 16384
merylThreads = 8

ovlStoreMemory = 16384

# grid info
useGrid = 0
scriptOnGrid = 0
frgCorrOnGrid = 0
ovlCorrOnGrid = 0

sge = -S /bin/bash -V -q all.q
#sge = -S /bin/bash -sync y -V -q all.q
sgeScript = -pe threads 1
sgeConsensus = -pe threads 1
sgeOverlap = -pe threads 4
sgeFragmentCorrection = -pe threads 4
sgeOverlapCorrection = -pe threads 1

#ovlHashBits = 22
#ovlHashBlockLength = 46871347
#ovlRefBlockSize =  537

ovlHashBits = 25
ovlThreads = 4
ovlHashBlockLength = 50000000
ovlRefBlockSize =  100000000

ovlConcurrency = 6
frgCorrThreads = 4
frgCorrBatchSize = 100000
ovlCorrBatchSize = 100000

cnsMinFrags = 7500
cnsConcurrency = 24

# change sgeName every time if you do not want to wait for the jobs not necessary to wait
sgeName = iroha
