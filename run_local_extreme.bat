@echo off
REM Wait for current local frontier to finish, then run extreme push (L=50, 80, 100).
:wait_loop
tasklist /FI "WINDOWTITLE eq dwave_b1_tfim*" 2>nul | find /I "dwave_b1_tfim_spin_glass.exe" >nul
if not errorlevel 1 (
    timeout /t 30 /nobreak >nul
    goto wait_loop
)
echo Frontier done at %DATE% %TIME%, starting LOCAL EXTREME push
cd /d C:\Users\ripva\Desktop\isomorphic-engine

REM Local 5070 Ti extreme push: L=50 (N=125K), L=60 (N=216K), L=80 (N=512K).
REM Fast preset (2K steps × 4 restarts) to keep wall-time reasonable at huge N.
target\release\examples\dwave_b1_tfim_spin_glass.exe ^
    --L 50,60,80 --seeds 0,1,2,3 --preset fast --with-gpu --sa-baseline ^
    --out paper_dsc3_vs_dwave\results\b1_local_extreme.json > paper_dsc3_vs_dwave\results\b1_local_extreme.log 2>&1

echo All done at %DATE% %TIME%
