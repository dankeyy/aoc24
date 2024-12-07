defmodule Day01 do
  def to_int(str) do
    case Integer.parse(str) do
      {int, _} -> int
      :error -> nil
    end
  end


  def insert_in_order(list, int) do
    {left, right} = Enum.split_while(list, &(&1 <= int))
    left ++ [int] ++ right
  end


  def sum_diffs({left, right}) do
    Enum.zip(left, right)
    |> Enum.map(fn {a, b} -> abs(b - a) end)
    |> Enum.sum
  end


  def similarity_score({left, right}) do
    frequencies = Enum.frequencies(right)
    Enum.reduce(left, 0, fn i, acc -> acc +  (i * Map.get(frequencies, i, 0)) end)
  end

  def solve(file_path) do
    File.read!(file_path)
    |> String.split("\n", trim: true)
    |> Enum.map(&String.split(&1, ~r/\s+/))
    |> Enum.reduce({[], []}, fn [l, r], {left_acc, right_acc} ->
      {insert_in_order(left_acc, to_int(l)), insert_in_order(right_acc, to_int(r))}
    end)
    |> then(fn columns ->
      {
        {:part1, sum_diffs(columns)},
        {:part2, similarity_score(columns)}
      }
    end)
  end

end

result = Day01.solve("day01.txt")
IO.inspect(result, label: "Solutions")
