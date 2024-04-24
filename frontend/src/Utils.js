export function nullToX(object, x) {
  return Object.fromEntries(
    Object.entries(object).map(([key, val]) => [key, val ? val : x]),
  );
}
