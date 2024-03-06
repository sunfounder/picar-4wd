function mapRange(value, fromMin, fromMax, toMin, toMax) {
    let normalizedValue = (value - fromMin) / (fromMax - fromMin);
    return normalizedValue * (toMax - toMin) + toMin;
}