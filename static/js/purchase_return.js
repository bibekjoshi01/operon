document.addEventListener("DOMContentLoaded", function () {
  const $supplier = $("#id_supplier");
  const $purchase = $("#id_ref_purchase");

  if (!$supplier.length || !$purchase.length) return;

  $supplier.on("change", function () {
    const supplierId = this.value;

    if (!supplierId) return;

    $purchase.empty().trigger("change");

    fetch(`/purchase/purchase-by-supplier/?supplier=${supplierId}`)
      .then((res) => res.json())
      .then((data) => {
        data.results.forEach((item) => {
          const option = new Option(item.text, item.id, false, false);
          $purchase.append(option);
        });

        $purchase.trigger("change");
      })
      .catch((err) => console.error("AJAX error:", err));
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const $purchase = $("#id_ref_purchase");
  if (!$purchase.length) return;

  $purchase.on("change", function () {
    const purchaseId = this.value;
    if (!purchaseId) return;

    fetch(`/purchase/purchase-items-by-purchase/?purchase=${purchaseId}`)
      .then((res) => res.json())
      .then((data) => {

        const items = data.results;

        const tbody = document.querySelector("#purchase-items-table tbody");

        if (!tbody) {
          console.error("Table body not found");
          return;
        }

        // clear old rows
        tbody.innerHTML = "";

        items.forEach((item) => {

          const row = document.createElement("tr");

          row.innerHTML = `
            <td>${item.item_name ?? item.item_id}</td>
            <td>${item.quantity}</td>
            <td>${item.rate}</td>
            <td>${item.tax_rate}</td>
            <td>${item.discount_rate}</td>
            <td>${item.gross_amount}</td>
            <td>${item.net_amount}</td>
          `;

          tbody.appendChild(row);
        });

      })
      .catch((err) => console.error("API error:", err));
  });
});
