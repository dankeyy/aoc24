import Control.Monad (replicateM)


data ParsedLine = ParsedLine
    { total    :: Integer
    , elements :: [Integer]
    } deriving (Show)


parse line = ParsedLine{ total = head parsed, elements = tail parsed}
  where
    parsed = map read $ words $ replaceChar ':' ' ' line :: ([Integer])
    replaceChar old new = map (\c -> if c == old then new else c)


applyCombination [x] [] = x
applyCombination (x:y:remainingOperands) (operator:remainingOperators) =
  applyCombination (operator x y : remainingOperands) remainingOperators


applyCombinations operands operators =
  [applyCombination operands operatorsCombination | operatorsCombination <- combinations]
  where
    combinations = generateCombinations $ length operands
    generateCombinations operandsAmount = replicateM (operandsAmount - 1) operators


calibration operators ParsedLine{total=result, elements=operands} =
  let results = (applyCombinations operands operators)
  in if result `elem` results
  then result
  else 0


main :: IO ()
main = do
  contents <- readFile "day07.txt"
  print $ sum $ map ((calibration [(*), (+)])             . parse) . lines $ contents -- p1
  print $ sum $ map ((calibration [(*), (+), numsConcat]) . parse) . lines $ contents -- p2
  where
    numsConcat x y = x * (10 ^ numDigits y) + y
    numDigits n = floor (logBase 10 (fromIntegral n)) + 1
